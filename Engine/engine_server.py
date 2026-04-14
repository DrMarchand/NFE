#!/usr/bin/env python3
import os
import json
from datetime import datetime
from ionic_gears import run_ionic_layer
from SynthesisGear import SynthesisGear

class NeuroForgeEngine:
    def __init__(self):
        self.modules = {}
        self.log_dir = os.path.expanduser("~/lab/ORCHARD/Intelligence/")
        os.makedirs(self.log_dir, exist_ok=True)

    def register(self, name, module):
        self.modules[name] = module
        print(f"⚙︎ [REGISTERED] {name}")

    def run(self, input_data):
        module_name = input_data.get("type")
        if module_name not in self.modules:
            return {"error": f"Module '{module_name}' not found"}

        result = self.modules[module_name].execute(input_data)
        self.log(module_name, result)
        return result

    def log(self, module, data):
        log_path = os.path.join(self.log_dir, "engine.log")
        with open(log_path, "a") as f:
            f.write(f"{datetime.now()} | {module} | {json.dumps(data)}\n")

# --- Sovereign Modules ---

class IdentityModule:
    def execute(self, input_data):
        return {"status": "ok", "identity": "Sovereign-786", "user": input_data.get("user", "default")}

class SynthesisModule:
    def execute(self, input_data):
        # Ties into your existing SynthesisGear logic
        node_path = input_data.get("node_path")
        if not node_path: return {"error": "No node_path provided"}
        syn = SynthesisGear(node_path)
        path = syn.execute()
        return {"status": "synthesized", "ledger": path}

if __name__ == "__main__":
    engine = NeuroForgeEngine()
    engine.register("identity", IdentityModule())
    engine.register("synthesis", SynthesisModule())
    
    # Listen for input
    try:
        import sys
        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {"type": "identity"}
        print(json.dumps(engine.run(input_data), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
