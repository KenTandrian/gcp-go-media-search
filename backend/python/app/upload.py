import os
from fastapi import UploadFile, HTTPException
from google.cloud import storage
from typing import List

class GCSUploader:
    def __init__(self, client: storage.Client, bucket_name: str):
        self.client = client
        self.bucket_name = bucket_name

    def upload_files(self, files: List[UploadFile]):
        """
        Uploads a list of files to the configured GCS bucket.
        """
        bucket = self.client.bucket(self.bucket_name)
        uploaded_filenames = []

        for file in files:
            try:
                # In a real application, you might want to stream the upload
                # rather than reading the whole file into memory.
                contents = file.file.read()
                blob = bucket.blob(file.filename)
                
                # Rewind the file pointer in case it's read again
                file.file.seek(0)

                content_type = file.content_type if file.content_type else "application/octet-stream"
                blob.upload_from_string(contents, content_type=content_type)
                uploaded_filenames.append(file.filename)
            except Exception as e:
                # In a real app, you'd have more robust error handling
                print(f"Failed to upload {file.filename}: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}")

        return {"message": f"Successfully uploaded {len(uploaded_filenames)} files.", "filenames": uploaded_filenames}
