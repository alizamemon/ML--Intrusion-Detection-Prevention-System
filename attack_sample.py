import pandas as pd

# load test data (unseen data)
test_path = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\test.csv"
df = pd.read_csv(test_path)

# sirf attack rows lo
attack_df = df[df[" Label"] == 1]

# label hata do (detection ke liye)
attack_df = attack_df.drop(" Label", axis=1)

# thori si rows sample kar lo
attack_df.sample(200).to_csv(
    r"F:\Web development\python\ML-ANSS\attack_sample.csv",
    index=False
)

print("✅ attack_sample.csv created successfully!")
