from google.cloud import bigquery
from typing import Optional
from . import models

class MediaService:
    def __init__(self, client: bigquery.Client, dataset_name: str, media_table: str):
        self.client = client
        self.dataset_name = dataset_name
        self.media_table = media_table

    def get_fqn(self) -> str:
        """Get the fully qualified table name."""
        table_ref = self.client.dataset(self.dataset_name).table(self.media_table)
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
            query_job = self.client.query(query, job_config=job_config)
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
            query_job = self.client.query(query, job_config=job_config)
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
