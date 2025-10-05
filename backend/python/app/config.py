from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or a .env file.
    """
    google_cloud_project: str = ""
    bigquery_dataset: str = "media_ds"
    bigquery_media_table: str = "media"
    bigquery_embeddings_table: str = "scene_embeddings"
    gcs_upload_bucket: str = ""
    signer_email: str = "" # The service account email to use for signing URLs

    # --- AI Model Settings ---
    summary_model_name: str = "gemini-2.5-pro"
    scene_script_model_name: str = "gemini-2.5-pro"
    embedding_model_name: str = "gemini-embedding-001"
    summary_prompt: str = """
Analyze the following media file and provide a summary in JSON format.
File: {media_url}

The JSON output should include the following fields:
- title (string)
- category (string, e.g., "movie", "trailer")
- summary (string)
- length_in_seconds (integer)
- cast (list of objects with "character_name" and "actor_name")
- scene_time_stamps (list of objects with "start" and "end" times in "HH:MM:SS" format)
"""
    scene_script_prompt: str = """
Analyze the scene from the media file '{media_url}' between {start} and {end}.
Provide a detailed script for this scene.
"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a single instance of the settings to be used throughout the application
settings = Settings()
