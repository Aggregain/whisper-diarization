from fastapi import FastAPI, UploadFile, File
import tempfile
from app.stt_pipeline import transcribe_audio
from app.diarization import diarize_audio, pipeline
from app.merge import merge_transcript_with_speakers
from app.schemas import TranscriptionResponse
import os

app = FastAPI()

@app.post("/v1/audio/transcriptions", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    audio = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio)
        tmp_path = tmp.name

    # Run Whisper transcription
    transcript_segments = transcribe_audio(tmp_path)

    diarization = pipeline({"audio": tmp_path})
    diarization_json = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarization_json.append({
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "speaker": speaker
        })

    # Merge transcript + diarization
    merged = merge_transcript_with_speakers(transcript_segments, diarization_json)

    # Format the merged list into a single text string with timestamps
    full_text_list = []
    for segment in merged:
        speaker_name = segment.get("speaker", "unknown")
        text = segment.get("text", "")
        start_time = segment.get("start")
        end_time = segment.get("end")

        # Format timestamps to HH:MM:SS format
        start_formatted = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}"
        end_formatted = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02}"

        # Combine speaker, timestamp, and text
        formatted_segment = f"[{start_formatted} - {end_formatted}] {speaker_name}: {text}"
        full_text_list.append(formatted_segment)

    full_text = "\n".join(full_text_list)

    # Clean up the temporary file
    os.unlink(tmp_path)

    return {
        "text": full_text,
        "files": []
    }