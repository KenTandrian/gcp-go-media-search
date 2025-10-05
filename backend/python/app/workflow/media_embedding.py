from google.cloud import bigquery
from .base import Chain
from .commands.scene_embedding_generator import SceneEmbeddingGenerator
from .commands.embedding_persist import EmbeddingPersistToBigQuery

def create_embedding_generation_chain(
    bq_client: bigquery.Client,
    dataset: str,
    table: str
) -> Chain:
    """
    Constructs the embedding generation chain.
    """
    embedding_chain = Chain(name="EmbeddingGenerationChain")

    # 1. Generate the vector embedding for the scene.
    generator_command = SceneEmbeddingGenerator(name="SceneEmbeddingGenerator")
    embedding_chain.add_command(generator_command)

    # 2. Persist the new embedding to BigQuery.
    persist_command = EmbeddingPersistToBigQuery(
        name="EmbeddingPersistToBigQuery",
        client=bq_client,
        dataset=dataset,
        table=table
    )
    embedding_chain.add_command(persist_command)

    return embedding_chain
