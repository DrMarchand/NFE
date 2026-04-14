#!/usr/bin/env python3
# ==========================================
# ⚙︎ Nɛuro-Forge Engine™ : Sovereign Core
# Identity : DrMarchand’s Lab⚛︎ratory™
# Purpose  : Master Receipt & Ledger Synthesis
# ==========================================

# --- STANDARD LIBRARY IMPORTS ---
import os
import json
from datetime import datetime, timezone

# --- EXTERNAL IMPORTS ---
import pandas as pd

# --- SOVEREIGN GEAR IMPORTS ---
from NexusGear import NexusGear

class EnginePanicError(Exception): pass

# ------------------------------
# ⚙︎ CONTAINERS & GEARS
# ------------------------------
class Box:
    def __init__(self):
        self.data = {
            "receiptId": None,
            "timestamp": None,
            "merchant_legalName": "Design Orchard LLC",
            "stripeChargeId": None,
            "grandTotal": None,
            "partner_id": None,          # Added Partner hook
            "labor_hours": None,
            "print_vendorJobId": None
        }

class InternalGear:
    def __init__(self, job_id):
        # 🟢 CLEAN CONNECTION: We just ask the Nexus for the data.
        self.nexus = NexusGear()
        self.system_state = self.nexus.get_internal_job(job_id)
        
    def inject(self, box):
        if self.system_state.get("labor"):
            box.data["labor_hours"] = self.system_state["labor"].get("hours")
        if self.system_state.get("structure"):
            box.data["print_vendorJobId"] = self.system_state["structure"].get("vendor_id")
        return box

class ValidatorGear:
    def audit(self, data):
        print("⚙︎ [VALIDATOR] Running clean audit...")
        if not data.get("receiptId"): raise EnginePanicError("Missing Receipt ID")
        print("🟩 [VALIDATOR] Passed")

# ------------------------------
# ⚙︎ RUNTIME EXECUTION
# ------------------------------
def run_engine(job_id):
    box = Box()
    
    # Inject Data
    box.data["receiptId"] = f"REC-{int(datetime.now(timezone.utc).timestamp())}"
    box = InternalGear(job_id).inject(box)
    
    # Audit
    ValidatorGear().audit(box.data)
    
    # Output
    os.makedirs('Gear_Box', exist_ok=True)
    df = pd.json_normalize(box.data)
    df.to_csv('Gear_Box/indesign_merge.csv', index=False)
    print("⚙︎ [$GEARBOX] Synthesis Complete. CSV Ready.")

if __name__ == "__main__":
    run_engine("job_001")
