def merge_transcript_with_speakers(transcript, diarization):
    merged = []
    for seg in transcript:
        speaker = "UNKNOWN"
        mid = (seg["start"] + seg["end"]) / 2
        for d in diarization:
            if d["start"] <= mid <= d["end"]:
                speaker = d["speaker"]
                break
        merged.append({
            "id": len(merged),
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"],
            "speaker": speaker
        })
    return merged
