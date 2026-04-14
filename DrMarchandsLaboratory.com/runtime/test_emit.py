import json
import os
import datetime
import random

# =====================================================================
# 🔬 DrMarchand’s Lab⚛︎ratory™
# Module: Manual Test Emitter
# =====================================================================

def fire_test_signal():
    print("📡 Forging test signal...")
    
    # 1. Forge a mock Genetic ID
    now = datetime.datetime.now()
    static_table = now.strftime("%Y%m%dT%H%M%S")
    tail = f"{now.microsecond:06d}{random.randint(0, 99):02d}"
    genetic_id = f"{static_table}.{tail}.mac.nfpro"
    
    # 2. Build the Payload
    signal = {
        "id": genetic_id,
        "cmd": "test_ping", # The Engine doesn't know this command yet!
        "user": "Kyle Marchand",
        "payload": {"message": "Hello from Lionheart Beta!"}
    }
    
    # 3. Drop it into the Signals folder
    signals_dir = "cloud_sync/signals"
    os.makedirs(signals_dir, exist_ok=True)
    
    filename = f"{genetic_id}.json"
    with open(os.path.join(signals_dir, filename), "w") as f:
        json.dump(signal, f, indent=2)
        
    print(f"✅ Signal dropped into Court: {filename}")

if __name__ == "__main__":
    fire_test_signal()

