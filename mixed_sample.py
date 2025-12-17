import pandas as pd

# paths
test_path = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\test.csv"
out_path  = r"F:\Web development\python\ML-ANSS\mixed_sample.csv"

# load test data
df = pd.read_csv(test_path)

# split benign & attack
benign = df[df[" Label"] == 0].sample(50, random_state=42)
attack = df[df[" Label"] == 1].sample(50, random_state=42)

# combine & shuffle
mixed = pd.concat([benign, attack]).sample(frac=1, random_state=42)

# REMOVE label (important!)
mixed = mixed.drop(columns=[" Label"])

mixed.to_csv(out_path, index=False)

print("✅ mixed_sample.csv created successfully!")
