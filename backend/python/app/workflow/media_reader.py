from google.cloud import bigquery
from .base import Chain
from .commands.media_trigger import MediaTriggerReader
from .commands.media_summary import MediaSummaryCreator
from .commands.media_summary_parser import MediaSummaryParser
from .commands.media_assembly import MediaAssembly
from .commands.media_persist import MediaPersistToBigQuery

def create_media_reader_chain(
    bq_client: bigquery.Client,
    dataset: str,
    table: str
) -> Chain:
    """
    Constructs the media reader chain for re-processing media.
    """
    reader_chain = Chain(name="MediaReaderChain")

    # 1. Read and parse the initial trigger message.
    reader_chain.add_command(MediaTriggerReader(name="MediaTriggerReader"))

    # 2. Generate a new high-level summary.
    reader_chain.add_command(MediaSummaryCreator(name="MediaSummaryCreator"))

    # 3. Parse the summary JSON.
    reader_chain.add_command(MediaSummaryParser(name="MediaSummaryParser"))

    # 4. Assemble the final Media object.
    reader_chain.add_command(MediaAssembly(name="MediaAssembly"))

    # 5. Persist the updated media object to BigQuery.
    reader_chain.add_command(MediaPersistToBigQuery(
        name="MediaPersistToBigQuery",
        client=bq_client,
        dataset=dataset,
        table=table
    ))

    return reader_chain
