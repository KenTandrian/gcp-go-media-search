import os
from google.cloud import storage

def get_gcs_parts(gcs_uri: str) -> tuple[str, str]:
    """
    Parses a GCS URI into its bucket and object name components.
    Example: "gs://my-bucket/my-folder/my-file.txt" -> ("my-bucket", "my-folder/my-file.txt")
    """
    if not gcs_uri.startswith("gs://"):
        raise ValueError(f"Invalid GCS URI format: {gcs_uri}")
    
    parts = gcs_uri[5:].split("/", 1)
    if len(parts) < 2:
        raise ValueError(f"Invalid GCS URI: unable to determine bucket and object from {gcs_uri}")
        
    bucket_name, object_name = parts
    return bucket_name, object_name

def create_gcs_uri(bucket: str, object_name: str) -> str:
    """
    Constructs a GCS URI from a bucket and object name.
    """
    return f"gs://{bucket}/{object_name}"
