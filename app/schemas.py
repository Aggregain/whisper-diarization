from typing import List, Optional
from pydantic import BaseModel


class Segment(BaseModel):
    id: int
    start: float
    end: float
    text: str
    speaker: Optional[str] = None


class TranscriptionResponse(BaseModel):
    id: str
    object: str = "transcription"
    model: str
    text: str
    segments: List[Segment]
