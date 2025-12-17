import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib

# Load data
train_path = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\train.csv"
test_path  = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\test.csv"

train_df = pd.read_csv(train_path)
test_df  = pd.read_csv(test_path)

# Split features & labels
X_train = train_df.drop(" Label", axis=1)
y_train = train_df[" Label"]

X_test  = test_df.drop(" Label", axis=1)
y_test  = test_df[" Label"]

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# APPLY SMOTE
print("\n Applying SMOTE to balance classes...")

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train_scaled, y_train
)

print("Before SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(pd.Series(y_train_resampled).value_counts())

# Train model on BALANCED data
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_resampled, y_train_resampled)

# Evaluate on UNSEEN test data
preds = model.predict(X_test_scaled)

print("\n Test Accuracy:", accuracy_score(y_test, preds))
print("\n Classification Report:\n")
print(classification_report(y_test, preds))

# Save model & scaler
save_dir = r"F:\Web development\python\ML-ANSS\MachineLearningCVE"

joblib.dump(model, save_dir + "\\rf_model.pkl")
joblib.dump(scaler, save_dir + "\\scaler.pkl")

print("\n Model trained with SMOTE & saved successfully!")
