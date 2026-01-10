# 🛡️ ML-Powered Intrusion Detection and Prevention System (IDPS)

## Problem Statement

Modern networks face an increasing number of cyberattacks such as DDoS, port scanning, and infiltration attempts. Traditional rule-based firewalls struggle to detect evolving attack patterns. This project addresses the problem by leveraging **Machine Learning** to intelligently detect malicious network traffic and automatically **prevent attackers in real time**.

---

## 📖 Project Overview

This project implements a complete **end-to-end Machine Learning–based Intrusion Detection and Prevention System (IDPS)** using network flow data from the **CICIDS 2017 dataset**.

A trained **Random Forest Classifier** analyzes network traffic and classifies it as either **BENIGN** or **ATTACK**. Once an attack is detected, a persistent **Prevention Module (IPS)** automatically blocks the malicious IP address. The entire system is visualized through a professional, interactive **Streamlit dashboard**.

This project demonstrates the **practical application of Machine Learning in cybersecurity**, bridging theory with real-world defense mechanisms.

---

## Core Components

1. **Detection (IDS):**
   - Random Forest classifier trained on CICIDS 2017 data
   - Handles class imbalance using **SMOTE**
   - High interpretability using feature importance

2. **Prevention (IPS):**
   - Automatically blocks attacking IPs
   - Maintains a persistent blacklist (`blocked_ips.csv`)
   - Simulates real firewall behavior

3. **Real-Time Dashboard:**
   - Built using **Streamlit**
   - Displays analytics, threats, and ML insights
   - Allows interactive IP blocking tests

---

##  Getting Started

### 1️⃣ Environment Setup

Create and activate a virtual environment, then install dependencies.

```bash
python -m venv .venv
.venv\Scripts\Activate

pip install pandas scikit-learn imbalanced-learn joblib streamlit numpy
```
### 2️⃣ Data Pipeline (One-Time Setup)
Run the following scripts in order to generate trained ML assets:

```bash
python step_merge.py
python step_clean.py
python step_split.py
python step_train.py
```
This will generate:
- rf_model.pkl → Trained Random Forest model
- scaler.pkl → Feature scaler

### 3️⃣ Detection & Prevention Simulation

Run the detection system on a mixed traffic sample:

```bash
python detection.py mixed_sample.csv
```
Malicious IPs are automatically added to: blocked_ips.csv

### 4️⃣ Launch the Dashboard

```bash
streamlit run dashboard.py
```

## 🖥️ Dashboard Features

### 📊 Network Analytics
-Total Flows
-Detected Attacks
-Threat Ratio

### Live IPS Report
-Attack severity visualization
-Real-time risk assessment

### ML Explainability
-Top feature importance chart
-Improves model transparency

### Flow-Level Inspection
-Filterable table of network flows
-Highlighted malicious traffic

### IPS Simulation
-Test if an IP is blocked
-Demonstrates prevention logic

### Screenshots
<img width="1365" height="626" alt="image" src="https://github.com/user-attachments/assets/93859e65-f07d-4f38-8315-18ecaf9e343b" />
<img width="1365" height="636" alt="image" src="https://github.com/user-attachments/assets/30c6fa51-25bf-4da1-a18d-f7c016bd3e2f" />
<img width="1365" height="637" alt="image" src="https://github.com/user-attachments/assets/713dbe9e-e3a5-4420-a925-2b8fee1a4bea" />

# 📈 Model Training & Evaluation Results

The **Random Forest** model was trained on the **CICIDS 2017** dataset, which exhibits a strong class imbalance between benign and attack traffic. To address this, **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to balance the dataset before training.



## 🔹 Class Distribution

### Before SMOTE:
* **BENIGN (0):** 1,818,663  
* **ATTACK (1):** 445,931

### After SMOTE:
* **BENIGN (0):** 1,818,663  
* **ATTACK (1):** 1,818,663

> This balancing step ensures that the model does not become biased toward the majority (benign) class and improves attack detection reliability.

---

## 🔹 Model Performance Metrics

* **Algorithm:** Random Forest Classifier
* **Class Balancing:** SMOTE
* **Dataset:** CICIDS 2017
* **Test Accuracy:** `99.89%`
* **Test Samples:** 566,149 network flows
* **False Positive Rate:** Low

### 🔹 Classification Report

| Class | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| **BENIGN (0)** | 1.00 | 1.00 | 1.00 | 454,434 |
| **ATTACK (1)** | 1.00 | 1.00 | 1.00 | 111,715 |
| | | | | |
| **Accuracy** | | | **0.999** | **566,149** |
| **Macro Avg** | 1.00 | 1.00 | 1.00 | 566,149 |
| **Weighted Avg** | 1.00 | 1.00 | 1.00 | 566,149 |

---

## 🔹 Key Observations

* **High Precision & Recall:** The model achieves near-perfect scores, indicating very low false positives and false negatives.
* **Effective Balancing:** SMOTE significantly improved the detection performance on minority attack traffic.
* **Explainability:** Feature importance analysis ensures the model is transparent and decisions are based on logical network flow patterns.

These results demonstrate that the system is **robust, reliable, and suitable** for real-world intrusion detection scenarios.

### Architecture Flow

<p align="center">
 <img width="881" height="578" alt="image" src="https://github.com/user-attachments/assets/c6e7d23f-2bb0-44be-ab6e-c9bba0a55443" />
</p>

### 📁 Project Structure

```text
ML-ANSS/
├── MachineLearningCVE/       # Folder for dataset and model assets
│   ├── rf_model.pkl          # Trained Random Forest model (Ignored by Git)
│   ├── scaler.pkl            # Trained data scaler (Ignored by Git)
│   └── (original dataset files)
├── blocked_ips.csv           # Persistent blacklist 
├── mixed_sample.csv          # Sample data for testing detection
├── dashboard.py              # Main Streamlit UI
├── detection.py              # Core ML detection logic
├── prevention.py             # IP blocking functions
├── step_merge.py             # Data Pipeline: Merging CSVs
├── step_clean.py             # Data Pipeline: Cleaning & Labeling
├── step_split.py             # Data Pipeline: Train/Test Split
├── step_train.py             # Data Pipeline: Model Training (SMOTE + RF)
└── README.md                 # Project documentation

```

###  Technology Stack

* **Language:** Python 3.10+
* **Machine Learning:** * `scikit-learn` (Random Forest Classifier)
    * `imbalanced-learn` (SMOTE for class balancing)
* **Data Processing:** `pandas`, `numpy`
* **Web Framework:** `Streamlit` (Interactive Dashboard)

---

###  Limitations & Future Work

While this system provides a robust baseline for ML-based security, the following enhancements are planned for future versions:

* **Real-Time Packet Capture:** Integration with `Scapy` or `PyShark` to analyze live network traffic instead of CSV files.
* **Advanced Architectures:** Implementing Deep Learning models like **LSTM** (for temporal patterns) and **Autoencoders** (for anomaly detection).
* **Hardware Integration:** Connecting the prevention module directly to system firewall rules (e.g., `iptables` on Linux or Windows Firewall API).
* **Multi-Class Classification:** Expanding the model to identify specific attack types (DDoS, PortScan, Infiltration) rather than just a binary "Attack" vs "Benign" label.
* **Cloud Deployment:** Containerizing the application using **Docker** for deployment on AWS or Azure Edge nodes.

### Disclaimer
This project is for educational and research purposes only.
It does not replace production-grade security systems.

#### Why This Project Matters
This system demonstrates how Machine Learning can enhance cybersecurity by enabling intelligent detection, automated prevention, and explainable decision-making — a critical need in modern digital infrastructure.

