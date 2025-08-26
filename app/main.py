from fastapi import FastAPI, UploadFile
import tempfile
from app.stt_pipeline import transcribe_audio
from app.diarization import diarize_audio
from app.merge import merge_transcript_with_speakers
from app.schemas import TranscriptionResponse

app = FastAPI()

@app.post("/v1/audio/transcriptions", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    transcript = transcribe_audio(tmp_path)
    diarization = diarize_audio(tmp_path)
    merged = merge_transcript_with_speakers(transcript, diarization)

    full_text = " ".join([seg["text"] for seg in merged])

    return TranscriptionResponse(
        id="transcript_01",
        model="whisper-large-v3",
        text=full_text,
        segments=merged
    )
