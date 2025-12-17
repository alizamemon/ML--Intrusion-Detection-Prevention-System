import pandas as pd
import glob
import os

folder = r"F:\Web development\python\ML-ANSS\MachineLearningCVE"

all_files = glob.glob(os.path.join(folder, "*.csv"))
print("Found files:", len(all_files))

dfs = []
for f in all_files:
    print("Loading:", os.path.basename(f))
    df = pd.read_csv(f, low_memory=False)   # low_memory=False helps avoid warning
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)
print("Combined shape (rows, cols):", data.shape)

out_path = os.path.join(folder, "CICIDS2017_combined.csv")
data.to_csv(out_path, index=False)
print("Saved combined CSV to:", out_path)
