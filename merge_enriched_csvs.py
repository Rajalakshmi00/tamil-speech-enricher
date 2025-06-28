# scripts/merge_enriched_csvs.py

import pandas as pd
from pathlib import Path

# Folder containing enriched CSVs
enriched_dir = Path("enriched")
merged_output_path = Path("final_output.csv")

# Read and merge all enriched files
all_dfs = []
for file in sorted(enriched_dir.glob("enriched_*.csv")):
    df = pd.read_csv(file)
    df["source_file"] = file.name  # optional: track which chunk this came from
    all_dfs.append(df)

# Concatenate into one DataFrame
merged_df = pd.concat(all_dfs, ignore_index=True)

# Sort by timestamp if needed (optional)
merged_df = merged_df.sort_values(by="start_time").reset_index(drop=True)

# Save to final output CSV
merged_df.to_csv(merged_output_path, index=False)
print(f"✅ Final merged CSV saved as: {merged_output_path}")
