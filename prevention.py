import pandas as pd
from datetime import datetime

BLOCKED_FILE = r"F:\Web development\python\ML-ANSS\blocked_ips.csv"

def block_ip(ip):
    try:
        df = pd.read_csv(BLOCKED_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["IP_Address", "Blocked_At"])

    if ip not in df["IP_Address"].values:
        df.loc[len(df)] = [ip, datetime.now()]
        df.to_csv(BLOCKED_FILE, index=False)
        print(f"IP Blocked: {ip}")
    else:
        print(f"⚠ IP already blocked: {ip}")
