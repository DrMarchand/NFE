#!/usr/bin/env python3
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ScoringGear import ScoringGear
from ExecutionGear import ExecutionGear
from SynthesisGear import SynthesisGear
from GitGear import GitGear


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


class EngineEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.execution_gear = ExecutionGear()
        self.git_gear = GitGear()

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return

        filename = os.path.basename(event.src_path)
        print(f"\n⚡ [NFE WATCHDOG] Node event: {filename}")
        time.sleep(0.1)

        gear = ScoringGear(event.src_path)
        score = gear.calculate_score()

        if score >= 85:
            print("⚛︎ [SYNTHESIS] Processing Node financials...")
            syn = SynthesisGear(event.src_path)
            syn.execute()
            self.execution_gear.build_partner_environment(gear.partner)
            self.git_gear.chronicle(
                f"⚛︎ [SYNTHESIS] Node {filename} synthesized into configured workspace."
            )
        else:
            print(f"🛑 [ROUTING] Node {filename} below Tier 1 threshold.")


# Historical import compatibility only; this name does not convey authority.
SovereignEventHandler = EngineEventHandler


class WatchdogDaemon:
    def __init__(self):
        self.watch_dir = required_path("NFE_NODES_ROOT")
        self.observer = Observer()
        self.handler = EngineEventHandler()

    def start(self):
        self.observer.schedule(self.handler, self.watch_dir, recursive=False)
        self.observer.start()
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🦮 [NFE WATCHDOG] Configured watch established")
        print("📂 Guarding configured Node directory")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    WatchdogDaemon().start()
