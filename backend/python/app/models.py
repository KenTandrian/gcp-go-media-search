from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Actor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    create_date: datetime = Field(default_factory=datetime.now)
    name: str
    date_of_birth: Optional[datetime] = None
    date_of_death: Optional[datetime] = None
    place_of_birth: Optional[str] = None
    biography: Optional[str] = None
    aliases: List[str] = []
    awards: List[str] = []
    nominations: List[str] = []
    image_url: Optional[str] = None

class CastMember(BaseModel):
    character_name: str
    actor_name: str

class Scene(BaseModel):
    sequence_number: int = Field(..., alias='sequence')
    tokens_to_generate: Optional[int] = None
    tokens_generated: Optional[int] = None
    start: str
    end: str
    script: str

class Media(BaseModel):
    id: str
    create_date: datetime = Field(default_factory=datetime.now)
    title: str
    category: str
    summary: str
    length_in_seconds: int
    media_url: str
    director: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[str] = None
    cast: List[CastMember] = []
    scenes: List[Scene] = []

    @staticmethod
    def new_media(file_name: str):
        generated_id = str(uuid.uuid5(uuid.NAMESPACE_URL, file_name))
        return Media(id=generated_id, title="", category="", summary="", length_in_seconds=0, media_url="")

class SceneEmbedding(BaseModel):
    id: str
    sequence_number: int
    model_name: str
    embeddings: List[float] = []

# Transient Models

class MediaFormatFilter(BaseModel):
    format: str
    width: str

class TimeSpan(BaseModel):
    start: str
    end: str

class MediaSummary(BaseModel):
    title: str
    category: str
    summary: str
    length_in_seconds: int
    media_url: Optional[str] = None
    director: Optional[str] = None
    release_year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[str] = None
    cast: List[CastMember] = []
    scene_time_stamps: List[TimeSpan] = []

class SceneMatchResult(BaseModel):
    media_id: str
    sequence_number: int
