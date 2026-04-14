import os
import json

# =====================================================================
# ⚙︎ Nɛuro-Forge Engine™ : Genesis Actuator
# Protocol: Matter Lookup (Periodic Table)
# =====================================================================

ACTUATOR_NAME = "Matter Lookup Tool"
COMMAND_BINDING = "lookup_element"
PERIODIC_TABLE_PATH = "cloud_sync/BOOKSHELF/notebooks/001_periodic_table.json"

def execute(bus_payload):
    """
    Input: {"cmd": "lookup_element", "payload": {"symbol": "C"}}
    """
    data = bus_payload.get("payload", {})
    symbol = data.get("symbol")
    
    if not symbol:
        return {"status": "failure", "error": "No 'symbol' provided in payload."}
        
    if not os.path.exists(PERIODIC_TABLE_PATH):
        return {"status": "failure", "error": "Periodic Table notebook offline."}
        
    with open(PERIODIC_TABLE_PATH, "r") as f:
        notebook = json.load(f)
        
    elements = notebook.get("elements", {})
    
    if symbol in elements:
        element_data = elements[symbol]
        return {
            "status": "success",
            "action": COMMAND_BINDING,
            "target": symbol,
            "makeup": element_data.get("makeup"),
            "mass": element_data.get("mass", "Unknown")
        }
    else:
        return {"status": "failure", "error": f"Element '{symbol}' not found."}

