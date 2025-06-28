# scripts/format_youtube_timestamps.py

import pandas as pd

# Load the merged final output
df = pd.read_csv("final_output.csv")

# Convert minutes to YouTube HH:MM:SS format
def minutes_to_hhmmss(mins):
    total_seconds = int(mins * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Format each row
formatted_lines = []
for idx, row in df.iterrows():
    timestamp = minutes_to_hhmmss(row['start_time'])
    summary = row['summary']
    line = f"{timestamp} - {summary}"
    formatted_lines.append(line)

# Save as a text file
with open("youtube_timestamps.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(formatted_lines))

print("✅ YouTube-friendly timestamps saved to 'youtube_timestamps.txt'")
