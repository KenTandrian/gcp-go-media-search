from google.cloud import storage

class GCS:
    """
    A helper class for interacting with Google Cloud Storage.
    """
    def __init__(self, client: storage.Client):
        self.client = client

    def get_bucket(self, bucket_name: str) -> storage.Bucket:
        """
        Gets a handle to a GCS bucket.
        """
        return self.client.bucket(bucket_name)

    def upload_from_file(self, local_file_path: str, bucket_name: str, object_name: str, content_type: str = "application/octet-stream"):
        """
        Uploads a local file to a GCS bucket.
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_filename(local_file_path, content_type=content_type)
        print(f"Successfully uploaded '{local_file_path}' to 'gs://{bucket_name}/{object_name}'.")

    def download_to_file(self, bucket_name: str, object_name: str, local_file_path: str):
        """
        Downloads an object from a GCS bucket to a local file.
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.download_to_filename(local_file_path)
        print(f"Successfully downloaded 'gs://{bucket_name}/{object_name}' to '{local_file_path}'.")
