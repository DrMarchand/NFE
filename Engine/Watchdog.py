#!/usr/bin/env python3
"""Read-only node observation. Execution requires a separate approval workflow."""

import hashlib
import json
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ScoringGear import ScoringGear


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


class EngineEventHandler(FileSystemEventHandler):
    """Observe nodes and emit proposals; never synthesize or mutate."""

    def __init__(self, watch_dir=None):
        root = watch_dir if watch_dir is not None else required_path("NFE_NODES_ROOT")
        self.watch_dir = os.path.realpath(root)

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return

        path = os.path.realpath(event.src_path)
        if os.path.dirname(path) != self.watch_dir:
            print("[WATCHDOG] Ignored path outside configured node directory")
            return

        try:
            # Reading and scoring only. No synthesis, partner writes, or Git.
            with open(path, "rb") as stream:
                payload = stream.read()
            digest = hashlib.sha256(payload).hexdigest()
            gear = ScoringGear(path)
            score = gear.calculate_score()
            proposal = {
                "kind": "node_observation",
                "filename": os.path.basename(path),
                "sha256": digest,
                "score": score,
                "suggested_operation": "synthesize" if score >= 85 else None,
                "approval_state": "awaiting_human_review" if score >= 85 else "not_proposed",
                "execution_performed": False,
            }
            print(json.dumps(proposal, ensure_ascii=False, sort_keys=True))
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print(f"[WATCHDOG] Observation failed: {type(exc).__name__}")


# Historical import compatibility only; this name does not convey authority.
SovereignEventHandler = EngineEventHandler


class WatchdogDaemon:
    def __init__(self):
        self.watch_dir = required_path("NFE_NODES_ROOT")
        self.observer = Observer()
        self.handler = EngineEventHandler(self.watch_dir)

    def start(self):
        self.observer.schedule(self.handler, self.watch_dir, recursive=False)
        self.observer.start()
        print("[WATCHDOG] Read-only node observation active")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    WatchdogDaemon().start()
