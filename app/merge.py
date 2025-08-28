def merge_transcript_with_speakers(transcript_segments, diarization):
    merged = []
    for t in transcript_segments:  # already a list of dicts
        speaker = None
        for d in diarization:
            if d['start'] <= t['start'] and t['end'] <= d['end']:
                speaker = d['speaker']
                break
        merged.append({
            "start": t['start'],
            "end": t['end'],
            "speaker": speaker or "unknown",
            "text": t['text']
        })
    return merged