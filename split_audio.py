from pydub import AudioSegment
import os
import math

def split_audio(input_file, chunk_length_minutes=30, output_folder="audio_chunks"):
    """
    Splits a large audio file into multiple chunks of specified minutes.

    Args:
    - input_file (str): path to your full-length audio file
    - chunk_length_minutes (int): length of each chunk in minutes
    - output_folder (str): folder where chunks will be saved

    Returns:
    - List of file paths for the audio chunks
    """
    os.makedirs(output_folder, exist_ok=True)

    audio = AudioSegment.from_file(input_file)
    chunk_length_ms = chunk_length_minutes * 60 * 1000  # convert to milliseconds
    total_chunks = math.ceil(len(audio) / chunk_length_ms)

    chunk_paths = []

    for i in range(total_chunks):
        start = i * chunk_length_ms
        end = min((i + 1) * chunk_length_ms, len(audio))
        chunk = audio[start:end]
        chunk_filename = os.path.join(output_folder, f"part{i + 1}.wav")
        chunk.export(chunk_filename, format="wav")
        chunk_paths.append(chunk_filename)
        print(f"Saved: {chunk_filename}")

    return chunk_paths
