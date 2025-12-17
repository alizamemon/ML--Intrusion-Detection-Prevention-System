import joblib

model = joblib.load(r"F:\Web development\python\ML-ANSS\MachineLearningCVE\rf_model.pkl")
scaler = joblib.load(r"F:\Web development\python\ML-ANSS\MachineLearningCVE\scaler.pkl")

print("MODEL EXPECTS THESE COLUMNS:\n")
print(scaler.feature_names_in_)
print("\nTotal:", len(scaler.feature_names_in_))
