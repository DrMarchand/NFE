#!/usr/bin/env python3
# ==========================================
# DrMarchand’s ⚙︎ Nɛuro-Forge Engine™ : Core
# Runtime context : 🔬 DrMarchand’s Lab⚛︎ratory™
# Purpose : Master Receipt & Ledger Synthesis
# ==========================================

import os
import json
from datetime import datetime, timezone

import pandas as pd

from NexusGear import NexusGear


class EnginePanicError(Exception):
    pass


class Box:
    def __init__(self):
        self.data = {
            "receiptId": None,
            "timestamp": None,
            "merchant_legalName": "Design Orchard LLC",
            "stripeChargeId": None,
            "grandTotal": None,
            "partner_id": None,
            "labor_hours": None,
            "print_vendorJobId": None,
        }


class InternalGear:
    def __init__(self, job_id):
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
        if not data.get("receiptId"):
            raise EnginePanicError("Missing Receipt ID")
        print("🟩 [VALIDATOR] Passed")


def run_engine(job_id):
    box = Box()

    box.data["receiptId"] = f"REC-{int(datetime.now(timezone.utc).timestamp())}"
    box = InternalGear(job_id).inject(box)

    ValidatorGear().audit(box.data)

    os.makedirs("Gear_Box", exist_ok=True)
    df = pd.json_normalize(box.data)
    df.to_csv("Gear_Box/indesign_merge.csv", index=False)
    print("⚙︎ [$GEARBOX] Synthesis Complete. CSV Ready.")


if __name__ == "__main__":
    run_engine("job_001")
