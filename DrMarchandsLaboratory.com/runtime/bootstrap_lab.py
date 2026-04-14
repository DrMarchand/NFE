import os
import json
import time
import datetime
import shutil
from actuator_registry import ActuatorRegistry

# =====================================================================
# ⚙︎ Nɛuro-Forge Engine™ : Sovereign Kernel (v5)
# Environment: Lionheart [Beta]
# =====================================================================

MAX_BATCH_SIZE = 99
CLOUD_SIGNAL_DIR = "cloud_sync/signals"
RECEIPT_DIR = "cloud_sync/receipts"
DLO_DIR = "cloud_sync/BOOKSHELF/dead_letters"
LOCAL_CURSOR_FILE = "runtime/cursor.json"

registry = ActuatorRegistry()

def shelve_dead_letter(filename, error_type, error_msg):
    src_path = os.path.join(CLOUD_SIGNAL_DIR, filename)
    error_id = filename.replace(".json", f".err_{error_type}.json")
    dst_path = os.path.join(DLO_DIR, error_id)
    
    try:
        shutil.move(src_path, dst_path)
        print(f"[⚠️ ISOLATED] Signal DLO'd: {error_id} | Reason: {error_msg}")
    except Exception as e:
        print(f"[☠️ PANIC] Failed to isolate {filename}: {e}")

def process_signal(filename):
    path = os.path.join(CLOUD_SIGNAL_DIR, filename)
    
    try:
        with open(path, "r") as f:
            payload = json.load(f)
    except Exception as e:
        return shelve_dead_letter(filename, "ingest_fail", e)

    try:
        result = registry.execute_instinct(payload)
    except Exception as e:
        return shelve_dead_letter(filename, "actuator_crash", e)

    receipt_name = filename.replace(".json", ".receipt.json")
    with open(os.path.join(RECEIPT_DIR, receipt_name), "w") as f:
        json.dump(result, f, indent=2)
    print(f"[✓ PROCESSED] ⚙︎ Receipt forged: {receipt_name}")

def engine_loop():
    print(f"[⚙︎ COURT] NFE [DLO Active] Online. Monitoring Lionheart [Beta] signals...")
    os.makedirs(CLOUD_SIGNAL_DIR, exist_ok=True)
    os.makedirs(DLO_DIR, exist_ok=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    
    while True:
        registry.refresh()
        signals = sorted([f for f in os.listdir(CLOUD_SIGNAL_DIR) if f.endswith(".json")])
        
        last_file = ""
        if os.path.exists(LOCAL_CURSOR_FILE):
            with open(LOCAL_CURSOR_FILE, "r") as f:
                last_file = json.load(f).get("last_file", "")
        
        new_signals = [s for s in signals if s > last_file]
        
        if not new_signals:
            time.sleep(1)
            continue
            
        buckets = [new_signals[i:i + MAX_BATCH_SIZE] for i in range(0, len(new_signals), MAX_BATCH_SIZE)]
        
        for bucket in buckets:
            for signal_file in bucket:
                process_signal(signal_file)
                with open(LOCAL_CURSOR_FILE, "w") as f:
                    json.dump({"last_file": signal_file}, f)
            time.sleep(1) # Refractory Period

if __name__ == "__main__":
    engine_loop()


