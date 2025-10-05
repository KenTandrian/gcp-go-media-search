from google.genai import Client
from ..base import Command, Context
from ... import models
from ...config import settings

class SceneExtractor(Command):
    """
    A command to extract a detailed script for each scene.
    """
    def __init__(self, name: str, media_param: str = "media"):
        super().__init__(name)
        self.media_param = media_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the Media object with scene time stamps exists in the context.
        """
        media = context.get(self.media_param)
        return media is not None and media.scenes is not None

    def execute(self, context: Context):
        """
        Generates a detailed script for each scene.
        
        NOTE: This is a placeholder. In a real application, this method would
        call a generative AI model to analyze each scene and produce a script.
        """
        print("Extracting detailed scene scripts with Gemini...")
        media = context.get(self.media_param)

        # Initialize the Vertex AI client.
        client = Client(vertexai=True, project=settings.google_cloud_project, location='global')

        for scene in media.scenes:
            prompt = settings.scene_script_prompt.format(
                media_url=media.media_url,
                start=scene.start,
                end=scene.end
            )
            try:
                response = client.models.generate_content(
                    model=settings.scene_script_model_name,
                    contents=prompt
                )
                scene.script = response.text.strip() if response.text else ""
                print(f"Generated script for scene {scene.sequence_number}.")
            except Exception as e:
                raise Exception(f"Failed to generate script for scene {scene.sequence_number}: {e}")

        print("Successfully extracted all scene scripts with Gemini.")
