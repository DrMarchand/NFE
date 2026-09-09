#!/usr/bin/env python3
import os
import json
from datetime import datetime
from SynthesisGear import SynthesisGear


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


class NeuroForgeEngine:
    def __init__(self):
        self.modules = {}
        self.log_dir = required_path("NFE_LOG_DIR")
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


class IdentityModule:
    def execute(self, input_data):
        return {
            "status": "ok",
            "identity": "system.engine",
            "display_name": "DrMarchand’s ⚙︎ Nɛuro-Forge Engine™",
            "user": input_data.get("user", "default"),
        }


class SynthesisModule:
    def execute(self, input_data):
        node_path = input_data.get("node_path")
        if not node_path:
            return {"error": "No node_path provided"}
        syn = SynthesisGear(node_path)
        path = syn.execute()
        return {"status": "synthesized", "ledger": path}


if __name__ == "__main__":
    engine = NeuroForgeEngine()
    engine.register("identity", IdentityModule())
    engine.register("synthesis", SynthesisModule())

    try:
        import sys

        raw_input = sys.stdin.read()
        input_data = json.loads(raw_input) if raw_input else {"type": "identity"}
        print(json.dumps(engine.run(input_data), indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
