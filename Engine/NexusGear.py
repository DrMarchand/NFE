#!/usr/bin/env python3
# ==========================================
# DrMarchand’s ⚙︎ Nɛuro-Forge Engine™ : NexusGear
# Purpose : Configured data connections and Atlas environment loading
# ==========================================
import json
import os
from dotenv import load_dotenv


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


class NexusGear:
    def __init__(self):
        # Private filesystem coordinates are supplied at runtime rather than
        # hardcoded into the public repository.
        self.orchard_root = required_path("NFE_ORCHARD_ROOT")
        self.atlas_path = required_path("NFE_ATLAS_ENV")

        if os.path.exists(self.atlas_path):
            load_dotenv(self.atlas_path)
        else:
            raise FileNotFoundError("Configured NFE_ATLAS_ENV does not exist")

    def get_partner(self, system_id):
        """Read a registered Node from the configured private data root."""
        filepath = os.path.join(self.orchard_root, "Nodes", f"{system_id}.json")
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ [NEXUS] Node {system_id} not found.")
            return None

    def save_partner(self, system_id, data):
        """Write a registered Node under the configured private data root."""
        filepath = os.path.join(self.orchard_root, "Nodes", f"{system_id}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as exc:
            print(f"🚨 [NEXUS] Node write error: {exc}")
            return False
