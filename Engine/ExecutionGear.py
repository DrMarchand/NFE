#!/usr/bin/env python3
# ==========================================
# ⚙︎ Nɛuro-Forge Engine™ : ExecutionGear
# Purpose : Physical File System Manipulation
# ==========================================
import os

class ExecutionGear:
    def __init__(self):
        self.projects_root = os.path.expanduser("~/lab/ORCHARD/Projects")

    def build_partner_environment(self, partner_data):
        name = partner_data.get("display_name", "Unknown_Partner")
        safe_name = name.replace(" ", "_").replace("/", "-")
        
        print(f"\n⚙︎ [EXECUTION] Forging physical workspace for: {name}")
        
        # 1. Define the physical territory
        partner_dir = os.path.join(self.projects_root, safe_name)
        assets_dir = os.path.join(partner_dir, "Assets")
        exports_dir = os.path.join(partner_dir, "Exports")
        
        # 2. Build the folders
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(exports_dir, exist_ok=True)
        print(f"   📂 Created: {partner_dir}")
        
        # 3. Drop the InDesign Base Tracker
        tracker_path = os.path.join(partner_dir, f"{safe_name}_ledger.csv")
        if not os.path.exists(tracker_path):
            with open(tracker_path, "w") as f:
                f.write("ProjectID,Glyphs_Produced,Labor_Hours,Status\n")
            print(f"   🧾 Initialized: {safe_name}_ledger.csv")
            
        print("🟩 [EXECUTION] Workspace fully established.")
        return partner_dir
