import pandas as pd
from sklearn.model_selection import train_test_split
import os

folder = r"F:\Web development\python\ML-ANSS\MachineLearningCVE"

clean = os.path.join(folder, "CICIDS2017_cleaned.csv")
train_out = os.path.join(folder, "train.csv")
test_out = os.path.join(folder, "test.csv")

print("Loading cleaned dataset...")
df = pd.read_csv(clean)

print("Splitting into train/test...")
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

train_df.to_csv(train_out, index=False)
test_df.to_csv(test_out, index=False)

print("\n DONE!")
print("Train saved at:", train_out)
print("Test saved at:", test_out)
