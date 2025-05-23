import time
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

import json

def load_dynamic_config():
    try:
        with open("node_example/config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("[WARN] Failed to load config.json:", e)
        return {}


load_dotenv()
# === CONFIGURATION ===
SERVER = os.getenv('BASE_URL')  # no trailing slash
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
NODE_ID = 1  # <-- ID of this node in the database

# === STEP 1: Authenticate and get token ===
def get_token():
    url = f"{SERVER}api-token-auth/"
    try:
        response = requests.post(url, json={"email": EMAIL, "password": PASSWORD})
        response.raise_for_status()  # This will raise an exception for 4xx/5xx status codes
        if response.status_code == 200:
            token = response.json()["token"]
            print("[INFO] Authenticated.")
            return token
    except requests.exceptions.RequestException as e:
        print("[ERROR] Failed to authenticate:", e)
    return None

# === STEP 2: Get own node info ===
def get_node_info(token):
    url = f"{SERVER}/api/nodes/{NODE_ID}/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("[ERROR] Failed to fetch node info:", response.text)
        return None

# === STEP 3: set node status to reading ===
def busy_node_status(token):
    url = f"{SERVER}/api/nodes/{NODE_ID}/"
    headers = {"Authorization": f"Token {token}"}
    data = {"status": "reading"}
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print("[INFO] Node status set to reading.")
    else:
        print("[ERROR] Failed to set status:", response.text)

# === STEP 3: Send a fake reading ===
def send_reading(token, node_id, dict):
    config = load_dynamic_config()
    headers = {"Authorization": f"Token {token}"}

    # Step 1: Get latest unfilled reading for this node
    get_url = f"{SERVER}/api/readings/latest/?node_id={node_id}"
    get_response = requests.get(get_url, headers=headers)

    if get_response.status_code != 200:
        print("[ERROR] No reading to update:", get_response.text)
        return False

    reading_id = get_response.json()["id"]
    patient_id = get_response.json()["patient"]
    timestamp = get_response.json()["timestamp"]

    # Step 2: Send PUT update
    put_url = f"{SERVER}/api/readings/{reading_id}/"
    if dict:
        data = dict
    else:
        data = {
            "timestamp": timestamp ,
            "temperature": config.get("temperature", 27),
            "alcohol": config.get("alcohol", 0.02),
            "urine": config.get("urine", 1),
            "berat": config.get("berat", 60),
            "tinggi": config.get("tinggi", 170),
            "patient_id": patient_id,
            "node": node_id
        }

    put_response = requests.put(put_url, json=data, headers=headers)
    if put_response.status_code == 200:
        print(f"[INFO] Updated reading {reading_id}.")
        return True
    else:
        print("[ERROR] Failed to update reading:", put_response.text)
        return False


# === STEP 4: Set node status back to idle ===
def reset_node_status(token):
    url = f"{SERVER}/api/nodes/{NODE_ID}/"
    headers = {"Authorization": f"Token {token}"}
    data = {"status": "available", "assigned_patient": None}
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print("[INFO] Node status reset to idle.")
    else:
        print("[ERROR] Failed to reset status:", response.text)

# === MAIN LOOP ===
def main():
    token = get_token()
    if not token:
        return

    while True:
        node_info = get_node_info(token)
        if not node_info:
            break  # Something went wrong

        status = node_info.get("status")
        patient_id = node_info.get("assigned_patient") 

        if status == "assigned" and patient_id:
            send_reading(token, NODE_ID, dict= {
            "temperature": None,
            "alcohol": None,
            "urine": None,
            "berat": None,
            "tinggi": None,
            "patient_id": patient_id,
            "node": NODE_ID
        })
            busy_node_status(token)
            print(f"[INFO] Assigned patient {patient_id}. Starting reading...")
            success = send_reading(token, NODE_ID, dict=False)
            if success:
                reset_node_status(token)
        else:
            print("[INFO] Waiting for job...")

        time.sleep(10)  # Wait before polling again

if __name__ == "__main__":
    main()
