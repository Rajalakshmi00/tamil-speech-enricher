import whisper
import pandas as pd
from pathlib import Path
import time
import threading
import sys
import os
from config import WHISPER_MODEL, CHUNK_DURATION, LANGUAGE

# Optional: Beep function (works on Windows)
def beep():
    if os.name == 'nt':
        import winsound
        winsound.Beep(1000, 300)  # frequency, duration in ms
    else:
        print('\a')  # Unix-style bell

# Timer thread to display live time + ETA
def live_timer(start_time, stop_event, estimated_time=None):
    while not stop_event.is_set():
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        line = f"\r⏱️ Elapsed: {mins:02d}:{secs:02d}"
        if estimated_time:
            eta = max(0, estimated_time - elapsed)
            eta_min, eta_sec = divmod(eta, 60)
            line += f" | ⌛ ETA: {eta_min:02d}:{eta_sec:02d}"
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(1)
    print()

# Folder setup
audio_dir = Path("audio_chunks")
output_dir = Path("transcripts")
output_dir.mkdir(exist_ok=True)

# Load Whisper model
print(f"📦 Loading Whisper model: {WHISPER_MODEL}")
model = whisper.load_model(WHISPER_MODEL)
print("✅ Model loaded.\n")

# Get audio files
audio_files = sorted(audio_dir.glob("*.wav"))
total_files = len(audio_files)

# For ETA calculation
time_per_file = []

for i, audio_file in enumerate(audio_files, start=1):
    print(f"\n🔁 [{i} / {total_files}] Transcribing: {audio_file.name}")

    start_time = time.time()
    stop_event = threading.Event()

    # Calculate estimated time (based on previous files)
    est = int(sum(time_per_file) / len(time_per_file)) if time_per_file else None

    # Start timer thread
    timer_thread = threading.Thread(target=live_timer, args=(start_time, stop_event, est))
    timer_thread.start()

    # Transcribe
    result = model.transcribe(
        str(audio_file),
        language=LANGUAGE,
        temperature=0.0,
        beam_size=5,
        best_of=5,
        fp16=False
    )

    # Stop timer
    stop_event.set()
    timer_thread.join()

    elapsed = int(time.time() - start_time)
    time_per_file.append(elapsed)

    print(f"✅ Done ({i} / {total_files}) — Took: {elapsed // 60}:{elapsed % 60:02d} min")
    beep()

    # Convert to DataFrame
    rows = []
    for seg in result['segments']:
        duration = seg["end"] - seg["start"]
        if duration >= CHUNK_DURATION:
            rows.append({
                "start_time": round(seg["start"] / 60, 2),
                "end_time": round(seg["end"] / 60, 2),
                "text": seg["text"].strip()
            })

    # Save
    if rows:
        df = pd.DataFrame(rows)
        out_csv = output_dir / f"transcript_{audio_file.stem}.csv"
        df.to_csv(out_csv, index=False)
        print(f"💾 Saved: {out_csv}")
    else:
        print(f"⚠️ No valid segments for {audio_file.name}")

print("\n🎉 All audio files transcribed successfully!")
