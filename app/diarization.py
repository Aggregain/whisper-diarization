from pyannote.audio import Pipeline
from app.config import Config

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token=Config.HF_TOKEN)

def diarize_audio(audio_path: str):
    diarization = pipeline(audio_path)
    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return results
