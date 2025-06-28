# scripts/enrich_with_tinyllama_optimized.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm  # 🟢 For progress tracking

# === 🧠 Load the local TinyLlama model ===
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print("⏳ Loading TinyLlama model... (small and CPU-friendly)")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # CPU only

# === 📂 Load input CSV ===
input_dir = Path("transcripts")
output_dir = Path("enriched_local")
output_dir.mkdir(parents=True, exist_ok=True)

for input_csv in sorted(input_dir.glob("*.csv")):
    print(f"\n📄 Processing file: {input_csv.name}")
    df = pd.read_csv(input_csv)

    summaries, questions, timestamps = [], [], []

    for index, row in tqdm(df.iterrows(), total=len(df), desc="🔁 Processing rows"):
        prompt = f"""
You are an assistant that processes Tamil spiritual speech.

Tamil Text:
\"\"\"{row['text']}\"\"\"

Tasks:
1. Give a 1–2 line summary in Tamil.
2. Ask 1–2 comprehension-style questions in English.

Format:
- Summary (Tamil): ...
- Questions (English): ...
"""

        try:
            result = generator(
                prompt,
                max_new_tokens=80,        # 🟢 Reduced token limit
                temperature=0.3,          # 🟢 Lower randomness
                top_k=30                  # 🟢 Restrict output diversity
            )[0]["generated_text"]

            if "Questions (English):" in result:
                summary = result.split("Questions (English):")[0].split("Summary (Tamil):")[-1].strip()
                ques = result.split("Questions (English):")[1].strip()
            else:
                summary, ques = "", ""

            # Format timestamp
            total_minutes = int(row['start_time'])
            seconds = int((row['start_time'] % 1) * 60)
            timestamp = f"{total_minutes:02d}:{seconds:02d}"

            summaries.append(summary)
            questions.append(ques)
            timestamps.append(timestamp)

            print(f"✅ Row {index} done")
            time.sleep(0.5)  # Slight delay for stability

        except Exception as e:
            print(f"❌ Error at row {index}: {e}")
            summaries.append("")
            questions.append("")
            timestamps.append("")

    # Save output
    df["timestamp"] = timestamps
    df["summary"] = summaries
    df["questions"] = questions
    output_file = output_dir / f"enriched_{input_csv.stem}.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Saved to: {output_file}")

print("🎉 All files enriched successfully!")
