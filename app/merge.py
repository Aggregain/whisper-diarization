def merge_transcript_with_speakers(transcript, diarization):
    merged = []
    for seg in transcript:
        # Find diarization label that overlaps with this segment
        speaker = "UNKNOWN"
        for d in diarization:
            if d["start"] <= seg["start"] and d["end"] >= seg["end"]:
                speaker = d["speaker"]
                break
        merged.append({
            "id": len(merged),
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "speaker": speaker
        })
    return merged
