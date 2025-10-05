from google.cloud import bigquery
from ..base import Command, Context
from ... import models

class MediaPersistToBigQuery(Command):
    """
    A command to save a Media object to a BigQuery table.
    """
    def __init__(self, name: str, client: bigquery.Client, dataset: str, table: str, media_param: str = "media"):
        super().__init__(name)
        self.client = client
        self.dataset = dataset
        self.table = table
        self.media_param = media_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the Media object to be persisted exists in the context.
        """
        return context.get(self.media_param) is not None

    def execute(self, context: Context):
        """
        Contains the core logic for writing the data to BigQuery.
        """
        print("Persisting media metadata to BigQuery...")
        media = context.get(self.media_param)
        
        if not isinstance(media, models.Media):
            raise TypeError("The 'media' object in the context is not of type models.Media")

        table_ref = self.client.dataset(self.dataset).table(self.table)
        
        # The BigQuery client library can automatically handle Pydantic models.
        errors = self.client.insert_rows_json(table_ref, [media.dict()])
        
        if errors:
            print(f"Failed to write media to database. Title: {media.title}, Errors: {errors}")
            raise Exception(f"BigQuery insert failed for title '{media.title}'")
        
        print(f"Successfully persisted media metadata for '{media.title}' (ID: {media.id})")
