from google.cloud import bigquery, storage
from ..services import MediaService
from ..search import SearchService
from ..upload import GCSUploader
from ..config import settings

class AppState:
    """
    A class to hold the global state of the application, including service clients.
    """
    def __init__(self):
        self.bq_client: bigquery.Client
        self.storage_client: storage.Client
        self.media_service: MediaService
        self.search_service: SearchService
        self.gcs_uploader: GCSUploader

    def initialize(self):
        """
        Initializes all the service clients and stores them in the state.
        """
        print("Initializing application state...")
        self.bq_client = bigquery.Client(project=settings.google_cloud_project)
        self.storage_client = storage.Client(project=settings.google_cloud_project)

        self.media_service = MediaService(
            client=self.bq_client,
            dataset_name=settings.bigquery_dataset,
            media_table=settings.bigquery_media_table
        )

        self.search_service = SearchService(
            client=self.bq_client,
            dataset_name=settings.bigquery_dataset,
            embeddings_table=settings.bigquery_embeddings_table
        )

        self.gcs_uploader = GCSUploader(
            client=self.storage_client,
            bucket_name=settings.gcs_upload_bucket
        )
        print("Application state initialized.")

# Create a single instance of the AppState to be used throughout the application
state = AppState()
