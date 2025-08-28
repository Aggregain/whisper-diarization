from pydantic import BaseModel
from typing import List

class TranscriptionResponse(BaseModel):
    text: str
    files: List[str] = [] # Keeping this field as it's required by your platform