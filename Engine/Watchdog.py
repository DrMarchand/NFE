#!/usr/bin/env python3
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ScoringGear import ScoringGear
from ExecutionGear import ExecutionGear
from SynthesisGear import SynthesisGear
from GitGear import GitGear

class SovereignEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.state_file = os.path.expanduser("~/lab/ORCHARD/Intelligence/processed_state.json")
        self.execution_gear = ExecutionGear()
        self.git_gear = GitGear()
        
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.json'):
            return
        
        filename = os.path.basename(event.src_path)
        print(f"\n⚡ [OS KERNEL] Node Injection: {filename}")
        time.sleep(0.1) # Buffer for file write
        
        # 1. Immune System (Scoring)
        gear = ScoringGear(event.src_path)
        score = gear.calculate_score()
        
        # 2. Synthesis (Financials & Ledgers)
        if score >= 85:
            print(f"⚛︎ [SYNTHESIS] Processing Node financials...")
            syn = SynthesisGear(event.src_path)
            syn.execute()
            self.execution_gear.build_partner_environment(gear.partner)
            
            # 3. Chronicle (GitHub Sync)
            self.git_gear.chronicle(f"⚛︎ [SYNTHESIS] Node {filename} synthesized into Orchard.")
        else:
            print(f"🛑 [ROUTING] Node {filename} below Tier 1 threshold.")

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
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    WatchdogDaemon().start()
