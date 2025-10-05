import os
from google.cloud import storage

def get_gcs_parts(gcs_uri: str) -> tuple[str, str]:
    """
    Parses a GCS URI into its bucket and object name components.
    It can handle both "gs://" and "https://storage.mtls.cloud.google.com/" formats.
    """
    if gcs_uri.startswith("gs://"):
        parts = gcs_uri[5:].split("/", 1)
    elif gcs_uri.startswith("https://storage.mtls.cloud.google.com/"):
        parts = gcs_uri[38:].split("/", 1)
    else:
        raise ValueError(f"Invalid GCS URI format: {gcs_uri}")

    if len(parts) < 2:
        raise ValueError(f"Invalid GCS URI: unable to determine bucket and object from {gcs_uri}")

    bucket_name, object_name = parts
    return bucket_name, object_name

def create_gcs_uri(bucket: str, object_name: str) -> str:
    """
    Constructs a GCS URI from a bucket and object name.
    """
    return f"gs://{bucket}/{object_name}"
