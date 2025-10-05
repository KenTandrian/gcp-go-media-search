from ..base import Command, Context
from ...cloud.gcs import GCS

class GcsFileUpload(Command):
    """
    A command to upload a local file to a GCS bucket.
    """
    def __init__(self, name: str, gcs_helper: GCS, bucket_name: str, local_file_path_param: str, remote_file_name_param: str):
        super().__init__(name)
        self.gcs_helper = gcs_helper
        self.bucket_name = bucket_name
        self.local_file_path_param = local_file_path_param
        self.remote_file_name_param = remote_file_name_param

    def is_executable(self, context: Context) -> bool:
        """
        Ensures that the local file path to be uploaded exists in the context.
        """
        return context.get(self.local_file_path_param) is not None

    def execute(self, context: Context):
        """
        Uploads the specified local file to the GCS bucket.
        """
        print("Uploading file to GCS...")
        local_path = context.get(self.local_file_path_param)
        remote_name = context.get(self.remote_file_name_param)

        if not remote_name:
            # If no remote name is specified, use the base name of the local file.
            import os
            remote_name = os.path.basename(local_path)

        try:
            self.gcs_helper.upload_from_file(
                local_file_path=local_path,
                bucket_name=self.bucket_name,
                object_name=remote_name
            )
            print(f"Successfully uploaded '{local_path}' to 'gs://{self.bucket_name}/{remote_name}'.")

        except Exception as e:
            raise Exception(f"Failed to upload file to GCS: {e}")
