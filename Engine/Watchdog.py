#!/usr/bin/env python3
# ==========================================
# ⚙︎ Nɛuro-Forge Engine™ : Phoenix Watchdog
# Purpose : OS-Level Event Triggers & JSON Memory
# ==========================================
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ScoringGear import ScoringGear
from ExecutionGear import ExecutionGear

class SovereignEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.state_file = os.path.expanduser("~/lab/ORCHARD/Intelligence/processed_state.json")
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        self.state = self.load_state()
        self.execution_gear = ExecutionGear()

    def load_state(self):
        """Loads synaptic memory."""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {}

    def save_state(self):
        """Commits reality to synaptic memory."""
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def on_created(self, event):
        """Triggered instantly by Mac OS when a file is created."""
        if event.is_directory or not event.src_path.endswith('.json'):
            return
            
        filename = os.path.basename(event.src_path)
        
        # Check permanent memory
        if filename in self.state:
            return
            
        print(f"\n⚡ [OS KERNEL EVENT] New Node Detected: {filename}")
        
        # Give the file system a millisecond to finish writing the file
        time.sleep(0.1) 
        
        # Route to Immune System
        gear = ScoringGear(event.src_path)
        score = gear.calculate_score()
        verdict = gear.verdict()
        print(f"⚖️ VERDICT: {verdict}")
        
        execution_path = None
        # Auto-Execution Route
        if score >= 85:
            print(f"🚀 [ROUTING] Node is Tier 1. Releasing ExecutionGear...")
            execution_path = self.execution_gear.build_partner_environment(gear.partner)
        else:
            print(f"🛑 [ROUTING] Node missed Tier 1. Holding execution.")
            
        # Burn to JSON Memory
        self.state[filename] = {
            "timestamp": int(time.time()),
            "score": score,
            "tier_verdict": verdict,
            "execution_path_generated": execution_path
        }
        self.save_state()

class WatchdogDaemon:
    def __init__(self):
        self.watch_dir = os.path.expanduser("~/lab/ORCHARD/Nodes/")
        self.observer = Observer()
        self.handler = SovereignEventHandler()

    def start(self):
        self.observer.schedule(self.handler, self.watch_dir, recursive=False)
        self.observer.start()
        
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🐕‍🦺 [PHOENIX WATCHDOG] OS-Level Hook Established")
        print(f"📂 Guarding Orbit: {self.watch_dir}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        try:
            while True:
                time.sleep(1) # Keeps the main thread alive while Observer runs in background
        except KeyboardInterrupt:
            self.observer.stop()
            print("\n🛑 [WATCHDOG] Disconnected from OS Kernel. Hibernating.")
        self.observer.join()

if __name__ == "__main__":
    WatchdogDaemon().start()
