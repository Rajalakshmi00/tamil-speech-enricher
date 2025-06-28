from split_audio import split_audio

# Replace with your audio path
input_audio_path = "audio/audio.mp3"

# Split into 30-minute chunks and save
chunks = split_audio(input_audio_path, chunk_length_minutes=30)

print("✅ Splitting done!")
print("Chunks created:", chunks)
