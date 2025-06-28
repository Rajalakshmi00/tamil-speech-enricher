🧠 Tamil Speech Enricher – Whisper-Based Transcript Summarizer
This project takes Tamil spiritual audio (like speeches or satsangs), transcribes them using Whisper, and enhances the result by generating:

✅ Short summaries in Tamil
✅ 1–2 comprehension-style questions in English
✅ YouTube-style timestamps for every speech chunk
Runs fully offline on CPU, using lightweight LLMs like TinyLlama or Phi-3, so you don’t need any OpenAI or Gemini API keys.

🔥 Key Features
🎧 Transcribes Tamil audio using Whisper
✍️ Adds Tamil summary + English questions for each chunk
⏱️ Generates timestamp (MM:SS format)
🧠 Works entirely on local models (no API rate limits)
💻 CPU-compatible (small models only)
🎯 Workflow
1. 🎙️ You upload a Tamil audio file manually
This can be .mp3, .wav, or any Whisper-compatible format.
(We don’t support YouTube download in this project — extract audio however you like.)

2. 🔤 Whisper transcribes it into transcripts/part_X.csv
Each row will contain:

start_time	text
1	Tamil sentence
2	Tamil sentence
3. 🧠 TinyLlama or Phi-3 processes it and adds:
Summary (Tamil)
Questions (English)
Timestamp (MM:SS)
4. 📤 Output is saved to enriched_local/enriched_part_X.csv
🛠 Setup
🔹 1. Install Requirements
pip install -r requirements.txt

🔹 2. Place Transcript CSVs
Add Whisper output files like:

transcripts/ ├── transcript_part_1.csv ├── transcript_part_2.csv

🔹 3. Run the Enricher Script
python scripts/enrich_with_tinyllama.py

You’ll get enriched CSVs in the enriched_local/ folder.

📦 File Structure
tamil-speech-enricher/ ├── transcripts/ # Whisper output │ └── transcript_part_1.csv ├── enriched_local/ # Output enriched CSVs ├── scripts/ │ └── enrich_with_tinyllama.py ├── requirements.txt └── README.md

💡 Sample Output Format
timestamp	text	summary	questions
00:45	Tamil sentence	சுருக்கம்	What is... Why...
💬 Notes
❗ We don’t include YouTube audio download (do it manually)
✅ Whisper-based transcription
✅ Runs offline (no cloud cost, no quota issues)
🐢 CPU inference is slow — patience is key!
🧠 Future Enhancements
Auto-chunk large audio into timed CSVs
Add optional Gemini/GPT mode
Export as subtitles or slides
👩‍💻 Author
Made with brain compression and CPU suffering by Rajalakshmi D If you love this, ⭐ star it or fork it — or hire me to write blogs 😄
