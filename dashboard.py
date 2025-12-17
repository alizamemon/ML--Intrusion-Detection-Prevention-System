import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# --- UI HELPERS ---
def highlight_attack(row):
    if row.Attack_Type == "ATTACK":
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)

# --- PATHS ---
MODEL_PATH = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\rf_model.pkl"
SCALER_PATH = r"F:\Web development\python\ML-ANSS\MachineLearningCVE\scaler.pkl"
DATA_PATH = r"F:\Web development\python\ML-ANSS\mixed_sample.csv"
BLOCKED_FILE = r"F:\Web development\python\ML-ANSS\blocked_ips.csv"

# --- CORE FUNCTIONS ---

@st.cache_resource
def load_assets():
    """Loads the model and scaler only once."""
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    except Exception as e:
        st.error(f"Error loading ML assets: {e}")
        return None, None

def get_blocked_ips():
    """Reads the persistent blocked IP list."""
    if os.path.exists(BLOCKED_FILE):
        return pd.read_csv(BLOCKED_FILE)['IP_Address'].tolist()
    return []

# --- STREAMLIT UI LAYOUT ---
st.set_page_config(layout="wide", page_title="IDPS Dashboard")


# SIDEBAR: LOGIN SIMULATION 

with st.sidebar:
    st.header("👤 User Login Simulation (IPS Test)")
    
    blocked_list = get_blocked_ips()
    
    with st.form("login_form"):
        st.write("Test if an IP address can access the system.")
        username = st.text_input("Username", value="admin")
        login_ip = st.text_input("Source IP to Test", value="10.0.0.5") # Default is the attacker IP
        submitted = st.form_submit_button("Attempt Login")
        
        if submitted:
            if login_ip in blocked_list:
                st.error(f"❌ LOGIN FAILED: IP {login_ip} is BLOCKED by the IPS Firewall.")
                st.caption("Access denied. The malicious IP cannot bypass the system.")
            else:
                st.success(f"✅ Login Successful for {username} from {login_ip}.")
                st.caption("IP not found in the blacklist.")
    
    st.markdown("---")
    st.subheader("🔒 Currently Blocked IPs")
    if blocked_list:
        st.dataframe(pd.DataFrame({"IP": blocked_list}), use_container_width=True)
    else:
        st.info("Blacklist is currently empty.")


#  MAIN DASHBOARD: DETECTION & ANALYTICS

model, scaler = load_assets()

if model and scaler is not None:
    st.title("🛡️ ML-Powered Intrusion Detection & Prevention System")
    st.markdown("---")

    # Load and process the sample data for analysis
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Data file not found at: {DATA_PATH}. Please run make_mixed_csv.py first.")
        st.stop()

    # Get the expected column names from the scaler
    expected_cols = list(scaler.feature_names_in_)
    # Rename columns in the loaded DataFrame to match the model's expected names
    df.columns = expected_cols  
    # 3. Clean
    df_features = df[expected_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    X_scaled = scaler.transform(df_features)
    preds = model.predict(X_scaled)
    
    df['Prediction'] = preds
    df['Attack_Type'] = df['Prediction'].map({0: "BENIGN", 1: "ATTACK"})
    
    # Simulate IP assignment 
    benign_ips = np.random.choice(['192.168.1.10', '172.16.0.4', '10.0.0.8'], size=len(df), replace=True)
    df["IP_Address"] = np.where(df["Prediction"] == 1, "10.0.0.5", benign_ips)
    
    #  Block status 
    blocked_list = get_blocked_ips()
    df["Blocked"] = df["IP_Address"].isin(blocked_list)
    
    # Metrics
    total_flows = len(df)
    attack_flows = df['Prediction'].sum()
    attack_ratio = attack_flows / total_flows if total_flows > 0 else 0
    
    st.header("Network Analytics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Flows Analyzed", total_flows)
    col2.metric("Detected Attack Flows", attack_flows, delta=f"{attack_ratio*100:.1f}% Threat Ratio")
    col3.metric("Attacker IP Found", len(df[df['Prediction'] == 1]['IP_Address'].unique()))
    
    st.markdown("---")


# LIVE IPS NARRATIVE REPORT
    st.header("Live IPS Report")

    if attack_flows > 0:
        attacker_ip = df[df["Prediction"] == 1]["IP_Address"].iloc[0]

        if attacker_ip in blocked_list:
            st.warning(
                f"🚨 ALERT: {attack_flows} malicious flows detected from {attacker_ip}. "
                f"STATUS: IP is already BLOCKED."
            )
        else:
            st.error(
                f"⚠️ ATTACK DETECTED: {attack_flows} flows from {attacker_ip}. "
                f"STATUS: Immediate blocking recommended."
            )
    else:
            st.success("✅ No malicious traffic detected. Network operating normally.")
            st.markdown("---")

            st.subheader("⚠️ Network Threat Level")

    threat_percent = attack_ratio * 100
    st.progress(int(threat_percent))
    st.caption(f"{threat_percent:.1f}% of total traffic classified as malicious")

    st.markdown("---")

    st.subheader("Top Attacking IPs")

    attack_ips = (
        df[df["Attack_Type"] == "ATTACK"]["IP_Address"]
        .value_counts()
    )

    if not attack_ips.empty:
        st.dataframe(
        attack_ips
        .rename("Attack Count")
        .reset_index()
        .rename(columns={"index": "IP Address"}),
        use_container_width=False,
        height=200
)

    else:
        st.info("No attacking IPs detected.")

    if st.button("🚫 Auto-Block All Attacking IPs"):
        attack_ips = df[df["Attack_Type"] == "ATTACK"]["IP_Address"].unique()
        pd.DataFrame({"IP_Address": attack_ips}).to_csv(BLOCKED_FILE, index=False)
        st.success("All attacking IPs have been blocked successfully!")

# 3. MACHINE LEARNING INSIGHTS

    st.header("Machine Learning Insights")

    feature_importances = pd.Series(
        model.feature_importances_,
        index=expected_cols
    )

    top_n = st.slider(
        "Select number of top features",
        min_value=5,
        max_value=20,
        value=10
    )

    importance_df = (
        feature_importances
        .nlargest(top_n)
        .reset_index()
    )

    importance_df.columns = ["Feature", "Importance"]
    importance_df["Feature"] = importance_df["Feature"].str.strip()

    st.subheader(f"Top {top_n} Features Influencing Detection")
    importance_df = importance_df.sort_values("Importance")

    st.line_chart(
    importance_df.set_index("Feature")["Importance"]
)


    st.caption(
        "These features contributed most to the Random Forest model's decision-making."
    )

    st.markdown("---")

    
    # Charts and Tables
    col_chart, col_table = st.columns(2)
    
    with col_chart:
        st.subheader("Traffic Distribution (Detection)")
        df_counts = df['Attack_Type'].value_counts().reset_index()
        df_counts.columns = ['Type', 'Count']
        st.bar_chart(df_counts, x='Type', y='Count', color='Type')

    with col_table:
        st.subheader("Flow Detail & Source IPs")

        filter_type = st.selectbox(
            "Filter Traffic",
            ["ALL", "ATTACK", "BENIGN"]
        )

        # Apply filter
        if filter_type == "ATTACK":
            view_df = df[df["Attack_Type"] == "ATTACK"]
        elif filter_type == "BENIGN":
            view_df = df[df["Attack_Type"] == "BENIGN"]
        else:
            view_df = df

        display_cols = ['IP_Address', 'Attack_Type', 'Blocked']
        display_cols += expected_cols[:2]

        rows_to_show = st.slider(
        "Number of flows to display",
        min_value=5,
        max_value=100,
        value=10,
        step=5
    )
        st.dataframe(
        view_df[display_cols]
        .sort_values(by="Attack_Type", ascending=False)
        .head(rows_to_show)
        .style.apply(highlight_attack, axis=1),
        use_container_width=True
    )

    with st.expander("📘 How This Intrusion Detection & Prevention System Works"):
        st.markdown("""
        **1️⃣ Detection**  
        Network traffic flows are analyzed using a trained Random Forest ML model.

        **2️⃣ Classification**  
        Each flow is classified as BENIGN or ATTACK.

        **3️⃣ Prevention**  
        Attacking IPs are added to a persistent blacklist.

        **4️⃣ Enforcement**  
        Blocked IPs are denied access during login attempts.

        **5️⃣ Real-World Application**  
        Suitable for SOC environments, automated IDS/IPS pipelines, and cybersecurity monitoring.
        """)


