import json
from google.genai import Client
from ..base import Command, Context
from ... import models
from ...config import settings

class MediaSummaryCreator(Command):
    """
    A command to generate a high-level summary of a media file.
    """
    def __init__(self, name: str, media_param: str = "media", summary_json_param: str = "summary_json"):
        super().__init__(name)
        self.media_param = media_param
        self.summary_json_param = summary_json_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the Media object exists in the context.
        """
        return context.get(self.media_param) is not None

    def execute(self, context: Context):
        """
        Generates a media summary and adds it to the context.
        
        NOTE: This is a placeholder. In a real application, this method would
        call a generative AI model to analyze the media and produce a summary.
        """
        print("Generating media summary with Gemini...")
        media = context.get(self.media_param)

        # Configure Google Gen AI Client
        client = Client(
            vertexai=True, project=settings.google_cloud_project, location='global'
        )


        # Construct the prompt from the settings
        prompt = settings.summary_prompt.format(media_url=media.media_url)

        try:
            response = client.models.generate_content(
                model=settings.summary_model_name,
                contents=prompt
            )
            # The response from the model may include markdown formatting for JSON,
            # so we need to clean it up.
            summary_json = response.text.strip().replace("```json", "").replace("```", "").strip() if response.text else ""
            
            # Validate that the output is valid JSON
            json.loads(summary_json)

            context.set(self.summary_json_param, summary_json)
            print("Successfully generated media summary JSON with Gemini.")
        except Exception as e:
            raise Exception(f"Failed to generate summary with Gemini: {e}")
