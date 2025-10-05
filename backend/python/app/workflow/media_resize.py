from .base import Chain
from ..cloud.gcs import GCS
from .commands.ffmpeg import TranscodeVideo
from .commands.gcs_download import GcsToTempFile
from .commands.media_cleanup import MediaCleanup
from .commands.gcs_file_upload import GcsFileUpload

def create_media_resize_chain(
    gcs_helper: GCS,
    output_bucket_name: str
) -> Chain:
    """
    Constructs the media resize chain.
    """
    resize_chain = Chain(name="MediaResizeChain")

    # 1. Download the original file.
    download_command = GcsToTempFile(
        name="GcsDownloadOriginal",
        gcs_helper=gcs_helper,
        media_param="source_media",
        temp_file_path_param="original_temp_path"
    )
    resize_chain.add_command(download_command)

    # 2. Transcode the file to a new size.
    transcode_command = TranscodeVideo(
        name="TranscodeToNewSize",
        temp_file_path_param="original_temp_path",
        transcoded_file_path_param="resized_temp_path"
    )
    resize_chain.add_command(transcode_command)

    # 3. Upload the resized file.
    upload_command = GcsFileUpload(
        name="GcsUploadResized",
        gcs_helper=gcs_helper,
        bucket_name=output_bucket_name,
        local_file_path_param="resized_temp_path",
        remote_file_name_param="resized_file_name"
    )
    resize_chain.add_command(upload_command)

    # 4. Clean up the temporary files.
    cleanup_command = MediaCleanup(
        "MediaCleanup",
        "original_temp_path",
        "resized_temp_path"
    )
    resize_chain.add_command(cleanup_command)

    return resize_chain
