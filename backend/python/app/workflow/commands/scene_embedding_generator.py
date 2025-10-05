from google.genai import Client
from ..base import Command, Context
from ... import models
from ...config import settings

class SceneEmbeddingGenerator(Command):
    """
    A command to generate a vector embedding for a scene's script.
    """
    def __init__(self, name: str, scene_param: str = "scene", embedding_param: str = "scene_embedding"):
        super().__init__(name)
        self.scene_param = scene_param
        self.embedding_param = embedding_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that a Scene object exists in the context.
        """
        return context.get(self.scene_param) is not None

    def execute(self, context: Context):
        """
        Generates an embedding for the scene's script.
        
        NOTE: This is a placeholder. In a real application, this method would
        call a machine learning model (e.g., Vertex AI) to get the vector embedding.
        """
        print("Generating scene embedding with Vertex AI...")
        scene = context.get(self.scene_param)
        media = context.get("media") # Assuming media object is in context

        if not isinstance(scene, models.Scene) or not isinstance(media, models.Media):
            raise TypeError("Invalid types for scene or media in context.")

        try:
            client = Client(vertexai=True, project=settings.google_cloud_project, location='global')
            # The embedding model is specified by its name.
            result = client.models.embed_content(
                model=settings.embedding_model_name,
                contents=scene.script,
            )

            if not result.embeddings or not result.embeddings[0].values:
                raise Exception("Failed to get embeddings from the model.")

            scene_embedding = models.SceneEmbedding(
                id=media.id,
                sequence_number=scene.sequence_number,
                model_name=settings.embedding_model_name,
                embeddings=result.embeddings[0].values
            )

            context.set(self.embedding_param, scene_embedding)
            print(f"Successfully generated embedding for scene {scene.sequence_number}.")
        except Exception as e:
            raise Exception(f"Failed to generate embedding for scene {scene.sequence_number}: {e}")
