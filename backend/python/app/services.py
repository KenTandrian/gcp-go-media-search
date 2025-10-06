from datetime import timedelta
from typing import Optional

import google.auth
from google.auth import impersonated_credentials
from google.cloud import bigquery, storage

from . import models
from .cloud import utils as cloud_utils
from .config import settings


class MediaService:
    def __init__(self, bq_client: bigquery.Client, storage_client: storage.Client, dataset_name: str, media_table: str):
        self.bq_client = bq_client
        self.storage_client = storage_client
        self.dataset_name = dataset_name
        self.media_table = media_table

    def generate_signed_url(self, gcs_uri: str, expires_in_minutes: int = 15) -> str:
        """Generates a time-limited, secure URL to access a private GCS object."""
        try:
            bucket_name, object_name = cloud_utils.get_gcs_parts(gcs_uri)
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(object_name)

            # Get the default credentials from the environment
            credentials, project_id = google.auth.default()

            # Create impersonated credentials
            target_credentials = impersonated_credentials.Credentials(
                source_credentials=credentials,
                target_principal=settings.signer_email,
                target_scopes=["https://www.googleapis.com/auth/devstorage.read_only"],
            )

            # Generate the signed URL
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(minutes=expires_in_minutes),
                method="GET",
                credentials=target_credentials,
            )
            return url
        except Exception as e:
            print(f"An error occurred while generating signed URL: {e}")
            raise

    def get_fqn(self) -> str:
        """Get the fully qualified table name."""
        table_ref = self.bq_client.dataset(self.dataset_name).table(self.media_table)
        return f"`{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`"

    def get(self, media_id: str) -> Optional[models.Media]:
        """Retrieves a single media object from BigQuery based on its unique ID."""
        query = f"SELECT * FROM {self.get_fqn()} WHERE id = @media_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("media_id", "STRING", media_id),
            ]
        )
        
        try:
            query_job = self.bq_client.query(query, job_config=job_config)
            results = query_job.result()

            row = None
            for r in results:
                row = r
                break

            if row is None:
                return None
            
            # Assuming the first row is the one we want
            row_dict = {key: value for key, value in row.items()}
            return models.Media(**row_dict)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_scene(self, media_id: str, scene_sequence: int) -> Optional[models.Scene]:
        """Retrieves a specific scene from a media object by its sequence number."""
        query = f"""
            SELECT s.*
            FROM {self.get_fqn()},
            UNNEST(scenes) as s
            WHERE id = @media_id AND s.sequence = @scene_sequence
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("media_id", "STRING", media_id),
                bigquery.ScalarQueryParameter("scene_sequence", "INTEGER", scene_sequence),
            ]
        )

        try:
            query_job = self.bq_client.query(query, job_config=job_config)
            results = query_job.result()

            row = None
            for r in results:
                row = r
                break

            if row is None:
                return None
            
            row_dict = {key: value for key, value in row.items()}
            return models.Scene(**row_dict)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
