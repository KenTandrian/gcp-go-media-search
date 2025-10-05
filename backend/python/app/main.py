from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from app.config import settings
from app.models import Media, Scene, SceneMatchResult
from app.telemetry import initialize_telemetry
from app.cloud.state import state
from typing import List

# --- Telemetry Initialization ---
initialize_telemetry()

# --- Application Setup ---
app = FastAPI()

# --- Service Initialization ---
state.initialize()


# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to confirm the server is running."""
    return {"status": "Media Search API is running"}

@app.get("/api/v1/media", response_model=List[Media])
def search_media(s: str = Query(..., min_length=1), count: int = Query(5, gt=0, le=20)):
    """Searches for media scenes based on a query string."""
    scene_results = state.search_service.find_scenes(s, count)
    if not scene_results:
        return []

    # Aggregate scenes by media ID to avoid duplicate media lookups
    media_map = {}
    for result in scene_results:
        if result.media_id not in media_map:
            media = state.media_service.get(result.media_id)
            if media:
                media.scenes = []  # Clear existing scenes to only show matched ones
                media_map[result.media_id] = media
        
        if result.media_id in media_map:
            scene = state.media_service.get_scene(result.media_id, result.sequence_number)
            if scene:
                media_map[result.media_id].scenes.append(scene)

    return list(media_map.values())

@app.get("/api/v1/media/{media_id}", response_model=Media)
def get_media_by_id(media_id: str):
    """Retrieve the full details of a specific media object by its ID."""
    media = state.media_service.get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@app.get("/api/v1/media/{media_id}/scenes/{scene_sequence}", response_model=Scene)
def get_scene_details(media_id: str, scene_sequence: int):
    """Fetch the details of a specific scene within a media object."""
    scene = state.media_service.get_scene(media_id, scene_sequence)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return scene

@app.get("/api/v1/media/{media_id}/stream")
def get_media_stream_url(media_id: str):
    """Generates a time-limited, signed URL for securely streaming a media file."""
    assert state.media_service is not None
    media = state.media_service.get(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    try:
        signed_url = state.media_service.generate_signed_url(media.media_url)
        return {"url": signed_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate streaming URL: {e}")

@app.post("/api/v1/uploads")
def upload_media_files(files: List[UploadFile] = File(...)):
    """Handles multipart/form-data file uploads to Google Cloud Storage."""
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided.")
    
    return state.gcs_uploader.upload_files(files)
