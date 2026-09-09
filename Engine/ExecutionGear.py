#!/usr/bin/env python3
# ==========================================
# DrMarchand’s ⚙︎ Nɛuro-Forge Engine™ : ExecutionGear
# Purpose : Authorized filesystem workspace preparation
# ==========================================
import os


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


class ExecutionGear:
    def __init__(self):
        self.projects_root = required_path("NFE_PROJECTS_ROOT")

    def build_partner_environment(self, partner_data):
        name = partner_data.get("display_name", "Unknown_Partner")
        safe_name = name.replace(" ", "_").replace("/", "-")

        print(f"\n⚙︎ [EXECUTION] Preparing workspace for: {name}")

        partner_dir = os.path.join(self.projects_root, safe_name)
        assets_dir = os.path.join(partner_dir, "Assets")
        exports_dir = os.path.join(partner_dir, "Exports")

        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(exports_dir, exist_ok=True)
        print(f"   📂 Created: {partner_dir}")

        tracker_path = os.path.join(partner_dir, f"{safe_name}_ledger.csv")
        if not os.path.exists(tracker_path):
            with open(tracker_path, "w") as f:
                f.write("ProjectID,Glyphs_Produced,Labor_Hours,Status\n")
            print(f"   🧾 Initialized: {safe_name}_ledger.csv")

        print("🟩 [EXECUTION] Workspace established.")
        return partner_dir
