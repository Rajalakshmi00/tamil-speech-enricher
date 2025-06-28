# transcribe_fast.py

from faster_whisper import WhisperModel
import pandas as pd
from pathlib import Path
from config import WHISPER_MODEL, LANGUAGE, CHUNK_DURATION

# Folders
audio_dir = Path("audio_chunks")
output_dir = Path("transcripts")
output_dir.mkdir(exist_ok=True)

# Load model
print(f"📦 Loading model: {WHISPER_MODEL}")
model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("✅ Model ready.\n")

# Transcribe each audio
for audio_file in sorted(audio_dir.glob("*.wav")):
    print(f"🔍 Transcribing: {audio_file.name}")

    segments, info = model.transcribe(
        str(audio_file),
        beam_size=5,
        language=LANGUAGE,
        vad_filter=True
    )

    rows = []
    for segment in segments:
        duration = segment.end - segment.start
        if duration >= CHUNK_DURATION:
            rows.append({
                "start_time": round(segment.start / 60, 2),
                "end_time": round(segment.end / 60, 2),
                "text": segment.text.strip()
            })

    if rows:
        df = pd.DataFrame(rows)
        out_path = output_dir / f"transcript_{audio_file.stem}.csv"
        df.to_csv(out_path, index=False)
        print(f"💾 Saved: {out_path}\n")
    else:
        print(f"⚠️ No valid segments for {audio_file.name}")
