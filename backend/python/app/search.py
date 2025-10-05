from google.cloud import bigquery
from typing import List
from . import models
from .config import settings
from google.genai import Client

# This is a placeholder for the actual query from the Go application.
# In a real application, this would be managed more robustly.
QRY_SEQUENCE_KNN = "SELECT base.media_id, base.sequence_number FROM VECTOR_SEARCH(TABLE `%s`, 'embeddings', (SELECT [ %s ] as embed), top_k => %d, distance_type => 'EUCLIDEAN') ORDER BY distance asc"

class SearchService:
    def __init__(self, client: bigquery.Client, dataset_name: str, embeddings_table: str):
        self.client = client
        self.dataset_name = dataset_name
        self.embeddings_table = embeddings_table

    def get_embeddings_fqn(self) -> str:
        """Get the fully qualified table name for the embeddings table."""
        table_ref = self.client.dataset(self.dataset_name).table(self.embeddings_table)
        return f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"

    def generate_embedding(self, query: str) -> List[float]:
        """
        Generates an embedding for the given query text using Vertex AI.
        """
        print(f"Generating embedding for query: '{query}'")
        try:
            client = Client(vertexai=True, project=settings.google_cloud_project, location='global')
            result = client.models.embed_content(
                model=settings.embedding_model_name,
                contents=query,
            )

            if not result.embeddings or not result.embeddings[0].values:
                raise Exception("Failed to get embeddings from the model.")

            return result.embeddings[0].values
        except Exception as e:
            raise Exception(f"Failed to generate embedding for query '{query}': {e}")

    def find_scenes(self, query: str, count: int) -> List[models.SceneMatchResult]:
        """
        Finds the most relevant scenes for a given query using vector search.
        """
        embedding = self.generate_embedding(query)
        embedding_str = ", ".join(map(str, embedding))
        
        sql = QRY_SEQUENCE_KNN % (self.get_embeddings_fqn(), embedding_str, count)
        
        try:
            query_job = self.client.query(sql)
            results = query_job.result()
            
            matches = []
            for row in results:
                matches.append(models.SceneMatchResult(
                    media_id=row.media_id,
                    sequence_number=row.sequence_number
                ))
            return matches
        except Exception as e:
            print(f"An error occurred during vector search: {e}")
            return []
