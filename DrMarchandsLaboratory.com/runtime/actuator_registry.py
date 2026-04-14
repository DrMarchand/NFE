import os
import importlib.util
import sys

# =====================================================================
# ⚙︎ Nɛuro-Forge Engine™ : Actuator Registry
# Protocol: The Instinct Bus Contract
# =====================================================================

ACTUATORS_DIR = "runtime/actuators"

class ActuatorRegistry:
    def __init__(self):
        self.actuators = {}
        os.makedirs(ACTUATORS_DIR, exist_ok=True)

    def refresh(self):
        """Hot-reloads all actuators in the Canopy."""
        self.actuators.clear()
        
        for filename in os.listdir(ACTUATORS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                path = os.path.join(ACTUATORS_DIR, filename)
                name = filename[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(name, path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, "COMMAND_BINDING") and hasattr(module, "execute"):
                        self.actuators[module.COMMAND_BINDING] = module
                except Exception as e:
                    print(f"[CANOPY ERROR] Failed to load {filename}: {e}")

    def execute_instinct(self, payload):
        """Routes a signal payload to the correct actuator via the Bus."""
        cmd = payload.get("cmd")
        
        if not cmd:
            raise ValueError("Payload missing 'cmd' binding.")
            
        if cmd not in self.actuators:
            raise NotImplementedError(f"No actuator registered for command: {cmd}")
            
        # Pass payload to the specific actuator's execute function
        return self.actuators[cmd].execute(payload)


