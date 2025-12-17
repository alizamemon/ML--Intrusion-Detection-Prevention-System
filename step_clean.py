import pandas as pd
import numpy as np
import os

folder = r"F:\Web development\python\ML-ANSS\MachineLearningCVE"
combined = os.path.join(folder, "CICIDS2017_combined.csv")
out_clean = os.path.join(folder, "CICIDS2017_cleaned.csv")

print("Loading and cleaning file in chunks...")

chunksize = 50000
cleaned_chunks = []

chunk_num = 1
for chunk in pd.read_csv(combined, chunksize=chunksize, low_memory=False):
    print(f"Processing chunk {chunk_num} ...")
    chunk_num += 1

    # Drop unwanted columns
    for col in ['Flow ID', 'Timestamp']:
        if col in chunk.columns:
            chunk = chunk.drop(columns=[col])

    # Replace inf & fill na
    chunk = chunk.replace([np.inf, -np.inf], np.nan).fillna(0)

    label_col = None
    for col in chunk.columns:
        if col.strip().lower() == "label":
            label_col = col
            break

    if label_col is None:
        print("⚠ No label column found in this chunk, skipping label conversion.")
    else:
        print(f"✔ Using label column: {label_col}")

        chunk[label_col] = chunk[label_col].astype(str)
        chunk[label_col] = chunk[label_col].apply(
            lambda x: 0 if x.strip().upper() == "BENIGN" else 1
        )

    cleaned_chunks.append(chunk)

print("Merging all cleaned chunks...")

final_df = pd.concat(cleaned_chunks, ignore_index=True)
final_df.to_csv(out_clean, index=False)

print("\n DONE! Cleaned file saved at:")
print(out_clean)
