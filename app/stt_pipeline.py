from faster_whisper import WhisperModel

whisper_model = WhisperModel("large", device="cuda", compute_type="float16")

def transcribe_audio(audio_path: str):
    segments, _ = whisper_model.transcribe(audio_path)
    results = []
    for seg in segments:
        results.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        })
    return results