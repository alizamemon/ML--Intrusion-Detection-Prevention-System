import sys
import pandas as pd
import joblib
import numpy as np
from prevention import block_ip

MODEL_PATH = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\rf_model.pkl"
SCALER_PATH = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("✔ Model & Scaler Loaded Successfully!")


if len(sys.argv) < 2:
    print("python detection.py file.csv")
    sys.exit()

csv_path = sys.argv[1]
print(f"\n Loading: {csv_path}")

df = pd.read_csv(csv_path)


expected_cols = list(scaler.feature_names_in_)

if " Label" in df.columns:
    df = df.drop(" Label", axis=1)

df.columns = expected_cols
df = df[expected_cols]

df = df.replace([np.inf, -np.inf], np.nan).fillna(0)


# Scale + Predict
X_scaled = scaler.transform(df)
preds = model.predict(X_scaled)

df["Prediction"] = preds
df["Attack_Type"] = df["Prediction"].map({0: "BENIGN", 1: "ATTACK"})

print("\n Detection Completed!\n")
print(df[["Prediction", "Attack_Type"]].head())
# .head() only 0-4 rows

# Assign IPs BASED ON MODEL PREDICTION
total_rows = len(df)

benign_ips = np.random.choice(
    ['192.168.1.10', '172.16.0.4', '10.0.0.8'],
    size=total_rows,
    replace=True
)

df["IP_Address"] = np.where(
    df["Prediction"] == 1,
    "10.0.0.5",     # attacker IP
    benign_ips
)


# TRIGGER PREVENTION (IPS)
detected_attack_flows_ips = df[df["Prediction"] == 1]["IP_Address"]
attack_ips = detected_attack_flows_ips.unique()

if len(attack_ips) > 0:
    print(f"\n DETECTED ATTACK FLOWS FROM IPs (Full List):\n{detected_attack_flows_ips.value_counts()}")
    print(f"\n ATTACKING IPs DETECTED: {len(attack_ips)} unique IPs found. Initiating block...")
    
    for ip in attack_ips:
        block_ip(ip)
else:
    print("\n No malicious IPs detected in this batch. No prevention action taken.")

# save
out = csv_path.replace(".csv", "_detected.csv")
df.to_csv(out, index=False)
print(f"\n📁 Saved as: {out}")

