from google.cloud import bigquery
from ..base import Command, Context
from ... import models

class EmbeddingPersistToBigQuery(Command):
    """
    A command to save a SceneEmbedding object to a BigQuery table.
    """
    def __init__(self, name: str, client: bigquery.Client, dataset: str, table: str, embedding_param: str = "scene_embedding"):
        super().__init__(name)
        self.client = client
        self.dataset = dataset
        self.table = table
        self.embedding_param = embedding_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the SceneEmbedding object to be persisted exists in the context.
        """
        return context.get(self.embedding_param) is not None

    def execute(self, context: Context):
        """
        Contains the core logic for writing the embedding data to BigQuery.
        """
        print("Persisting scene embedding to BigQuery...")
        embedding = context.get(self.embedding_param)
        
        if not isinstance(embedding, models.SceneEmbedding):
            raise TypeError("The 'scene_embedding' object in the context is not of type models.SceneEmbedding")

        table_ref = self.client.dataset(self.dataset).table(self.table)
        
        # The BigQuery client library can automatically handle Pydantic models.
        errors = self.client.insert_rows_json(table_ref, [embedding.dict()])
        
        if errors:
            print(f"Failed to write embedding to database. Media ID: {embedding.id}, Scene: {embedding.sequence_number}, Errors: {errors}")
            raise Exception(f"BigQuery insert failed for embedding of media '{embedding.id}', scene '{embedding.sequence_number}'")
        
        print(f"Successfully persisted embedding for media '{embedding.id}', scene '{embedding.sequence_number}'.")
