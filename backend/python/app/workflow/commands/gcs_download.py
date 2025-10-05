import os
import tempfile
from ...cloud.gcs import GCS
from ...cloud import utils as cloud_utils
from ..base import Command, Context
from ... import models

class GcsToTempFile(Command):
    """
    A command to download a media file from GCS to a local temporary file.
    """
    def __init__(self, name: str, gcs_helper: GCS, media_param: str = "media", temp_file_path_param: str = "temp_file_path"):
        super().__init__(name)
        self.gcs_helper = gcs_helper
        self.media_param = media_param
        self.temp_file_path_param = temp_file_path_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the Media object with a GCS URL exists in the context.
        """
        media = context.get(self.media_param)
        return media is not None and media.media_url is not None

    def execute(self, context: Context):
        """
        Downloads the file from GCS and stores the path to the temporary file in the context.
        """
        print("Downloading media file from GCS...")
        media = context.get(self.media_param)
        
        try:
            # Parse the GCS URI to get the bucket and object name
            bucket_name, object_name = cloud_utils.get_gcs_parts(media.media_url)

            # Create a temporary file and download the blob's content into it.
            _, temp_local_path = tempfile.mkstemp()
            self.gcs_helper.download_to_file(bucket_name, object_name, temp_local_path)

            context.set(self.temp_file_path_param, temp_local_path)
            print(f"Successfully downloaded '{media.media_url}' to '{temp_local_path}'.")

        except Exception as e:
            raise Exception(f"Failed to download file from GCS: {e}")
