import os
import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1, bigquery, storage
from .workflow.base import Context
from .workflow.media_processing import create_media_processing_chain
from .config import settings
from . import models

def pubsub_callback(message: pubsub_v1.types.pubsub_gapic_types.PubsubMessage) -> None:
    """
    Callback function for handling Pub/Sub messages.
    This function will be triggered when a new message is received.
    """
    print(f"Received Pub/Sub message: {message.data}")

    try:
        # Initialize the Google Cloud clients
        bq_client = bigquery.Client(project=settings.google_cloud_project)
        storage_client = storage.Client(project=settings.google_cloud_project)

        # Create the processing chain
        chain = create_media_processing_chain(
            bq_client=bq_client,
            storage_client=storage_client,
            dataset=settings.bigquery_dataset,
            table=settings.bigquery_media_table
        )

        # Create a new context and set the trigger message
        context = Context()
        context.set("trigger_message", message.data)

        # Execute the workflow
        chain.execute(context)

        if context.has_errors():
            print(f"Workflow completed with errors: {context.errors}")
            message.nack()
        else:
            print("Successfully processed Pub/Sub message.")
            message.ack()

    except Exception as e:
        print(f"An error occurred while processing Pub/Sub message: {e}")
        message.nack()

class PubSubListener:
    def __init__(self, project_id: str, subscription_id: str):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)

    def start(self):
        """
        Starts the Pub/Sub listener and begins pulling messages.
        """
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path, callback=pubsub_callback
        )
        print(f"Listening for messages on {self.subscription_path}...")

        # The future will block indefinitely unless there is an error.
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result() # Block until the cancellation is complete.
        except Exception as e:
            print(f"An error occurred with the Pub/Sub listener: {e}")
