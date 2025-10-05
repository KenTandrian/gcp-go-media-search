from google.cloud import bigquery, storage
from .base import Chain
from .commands.ffmpeg import TranscodeVideo
from .commands.gcs_download import GcsToTempFile
from .commands.media_assembly import MediaAssembly
from .commands.media_cleanup import MediaCleanup
from .commands.scene_extractor import SceneExtractor
from .commands.media_persist import MediaPersistToBigQuery
from .commands.media_summary import MediaSummaryCreator
from .commands.media_summary_parser import MediaSummaryParser
from .commands.media_trigger import MediaTriggerReader
from ..cloud.gcs import GCS

def create_media_processing_chain(
    bq_client: bigquery.Client,
    storage_client: storage.Client,
    dataset: str,
    table: str
) -> Chain:
    """
    Constructs the media processing chain with all its commands.
    """
    processing_chain = Chain(name="MediaProcessingChain")

    # Initialize cloud helpers
    gcs_helper = GCS(storage_client)

    # 1. Read and parse the initial trigger message.
    trigger_command = MediaTriggerReader(name="MediaTriggerReader")
    processing_chain.add_command(trigger_command)

    # 2. Download the media file from GCS to a temporary local file.
    download_command = GcsToTempFile(name="GcsToTempFile", gcs_helper=gcs_helper)
    processing_chain.add_command(download_command)

    # 3. Transcode the video to a standard format.
    transcode_command = TranscodeVideo(name="TranscodeVideo")
    processing_chain.add_command(transcode_command)

    # 4. Generate a high-level summary of the media.
    summary_command = MediaSummaryCreator(name="MediaSummaryCreator")
    processing_chain.add_command(summary_command)

    # 5. Parse the summary JSON into a MediaSummary object.
    parser_command = MediaSummaryParser(name="MediaSummaryParser")
    processing_chain.add_command(parser_command)

    # 6. Assemble the final Media object from the summary.
    assembly_command = MediaAssembly(name="MediaAssembly")
    processing_chain.add_command(assembly_command)

    # 7. Extract a detailed script for each scene.
    scene_extractor_command = SceneExtractor(name="SceneExtractor")
    processing_chain.add_command(scene_extractor_command)

    # As we convert more commands, they will be added here.

    # 8. Persist the final media object to BigQuery.
    persist_command = MediaPersistToBigQuery(
        name="MediaPersistToBigQuery",
        client=bq_client,
        dataset=dataset,
        table=table
    )
    processing_chain.add_command(persist_command)

    # Finally, clean up all temporary files.
    cleanup_command = MediaCleanup(
        "MediaCleanup",
        "temp_file_path",
        "transcoded_file_path"
    )
    processing_chain.add_command(cleanup_command)

    return processing_chain
