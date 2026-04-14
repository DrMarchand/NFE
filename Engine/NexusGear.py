#!/usr/bin/env python3
# ==========================================
# ⚙︎ Nɛuro-Forge Engine™ : NexusGear
# Purpose : Clean Database Connections & Atlas Env Loader
# ==========================================
import json
import os
from dotenv import load_dotenv

class NexusGear:
    def __init__(self):
        # 1. Define the physical architecture
        self.orchard_root = os.path.expanduser("~/lab/ORCHARD")
        
        # 2. Awaken Atlas
        self.atlas_path = os.path.expanduser("~/lab/ENGINE_ROOM/atlas.env")
        if os.path.exists(self.atlas_path):
            load_dotenv(self.atlas_path)
            # print("⚙︎ [NEXUS] Atlas Environment Online.")
        else:
            print("🚨 [NEXUS] WARNING: atlas.env not found in ENGINE_ROOM.")

    def get_partner(self, system_id):
        """Safely connects to the Nodes database."""
        filepath = os.path.join(self.orchard_root, "Nodes", f"{system_id}.json")
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ [NEXUS] Database miss: Node {system_id} not found.")
            return None

    def save_partner(self, system_id, data):
        """Safely writes to the Nodes database."""
        filepath = os.path.join(self.orchard_root, "Nodes", f"{system_id}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"🚨 [NEXUS] Database Write Error: {e}")
            return False
