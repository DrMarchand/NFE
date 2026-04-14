#!/usr/bin/env python3
# ==========================================
# ⚙︎ Nɛuro-Forge Engine™ : SynthesisGear
# Purpose : Chaining Ionic Calculus & Core Output
# ==========================================
import os
import json
import pandas as pd
from ionic_gears import run_ionic_layer
from core import Box, ValidatorGear

class SynthesisGear:
    def __init__(self, node_path):
        self.node_path = node_path
        with open(node_path, 'r') as f:
            self.node_data = json.load(f)

    def execute(self):
        print(f"⚛︎ [SYNTHESIS] Processing Node financials...")
        
        # 1. Run the Ionic Calculus (Margins/Costs)
        enriched_data = run_ionic_layer(self.node_data)
        
        # 2. Synthesize the Ledger/Receipt
        print(f"⚙︎ [CORE] Forging Ledger for {enriched_data.get('name')}...")
        os.makedirs('Gear_Box', exist_ok=True)
        
        # We use your existing Box logic
        df = pd.json_normalize(enriched_data)
        output_path = f"Gear_Box/{enriched_data.get('acronym', 'NODE')}_ledger.csv"
        df.to_csv(output_path, index=False)
        
        print(f"🟩 [SYNTHESIS] Complete. Output: {output_path}")
        return output_path

if __name__ == "__main__":
    # Test with an existing Node if available
    pass
