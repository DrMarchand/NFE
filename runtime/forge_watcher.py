import time
import subprocess
import json
from datetime import datetime

ENGINE_PATH = "core/engine/engine_server.py"
STATE_FILE = "runtime/state.json"
INTERVAL_SECONDS = 5


def log(msg):
    print(f"[WATCHER {datetime.now()}] {msg}")


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"cycle": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


import os
import json

SIGNAL_DIR = "runtime/signals"

def load_signals():
    signals = []

    if not os.path.exists(SIGNAL_DIR):
        return signals

    for file in os.listdir(SIGNAL_DIR):
        if file.endswith(".json"):
            path = os.path.join(SIGNAL_DIR, file)

            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    data["_file"] = file
                    signals.append(data)
            except:
                continue

    return signals

def decide(state):
    signals = load_signals()

    # 🔥 If there are commands, execute highest priority first
    if signals:
        signals.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return signals[0]

    # ⏱ fallback time logic
    from datetime import datetime
    hour = datetime.now().hour

    if 6 <= hour < 12:
        return {"type": "identity", "user": "morning-node"}
    elif 12 <= hour < 18:
        return {"type": "identity", "user": "day-node"}
    elif 18 <= hour < 24:
        return {"type": "identity", "user": "evening-node"}
    else:
        return {"type": "identity", "user": "night-node"}


def run_engine(input_payload):
    try:
        result = subprocess.run(
            ["python3", ENGINE_PATH],
            input=json.dumps(input_payload),
            capture_output=True,
            text=True
        )
        log(f"Executed with input: {input_payload}")
        print(result.stdout)
    except Exception as e:
        log(f"ERROR: {e}")


def main():
    log("Watcher started")

    while True:
        state = load_state()

        decision = decide(state)

        run_engine(decision)

        state["cycle"] += 1
        save_state(state)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()