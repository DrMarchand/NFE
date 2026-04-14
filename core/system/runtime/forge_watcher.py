#!/usr/bin/env python3
from pathlib import Path
import json
import os
import socket
import time

HEADER_FILE = Path.home() / ".neuro_forge_header"
BRIDGE_STATE_FILE = Path.home() / ".forge_bridge_state.json"
MESH_STATE_FILE = Path.home() / ".forge_mesh_state.json"
ATLAS_ENV_FILE = Path.home() / "atlas.env"

def load_env_file(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"')
    return env

ATLAS = load_env_file(ATLAS_ENV_FILE)

LIBRARY_REMOTE_HOST = ATLAS.get("ATLAS_VAULT_HOST_REMOTE", "ssh.drmarchandslaboratory.com")
LIBRARY_REMOTE_PORTS = [22, 445, 139]

LIBRARY_CANDIDATES = [
    Path(ATLAS.get("ATLAS_LIBRARY_PATH", "/Volumes/LAB_8TB/LIB_2TB")),
    Path(ATLAS.get("ATLAS_LIBRARY_ALIAS", str(Path.home() / "Shared" / "📚 DrMarchand’s ⚛︎ Library™"))),
]

WORKBENCH_CANDIDATES = [
    Path(ATLAS.get("ATLAS_WORKBENCH_PATH", "/Volumes/LAB_8TB/WORKBENCH")),
    Path(ATLAS.get("ATLAS_WORKBENCH_ALIAS", str(Path.home() / "Shared" / "🪑 DrMarchand’s ⚛︎ Workbench™"))),
]

REQUIRED_MMS_MARKERS = [
    "⚙︎",
    "MMS-768™",
    "© Design Orchard LLC",
    "🔬 DrMarchand’s Lab⚛︎ratory™",
    "📚 DrMarchand’s ⚛︎ Library™",
    "Self-taught. Not a doctor.",
    "Not an architect. Not licensed."
]

COLOR_MAP = {
    "NEXUS": "⬛",
    "GENESIS": "⬜",
    "BLUE": "🟦",
    "YELLOW": "🟨",
    "ORANGE": "🟧",
    "GREEN": "🟩",
    "PURPLE": "🟪",
    "RED": "🟥",
    "GRAY": "⬜⬛",
}

def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None

def first_existing_path(paths):
    for p in paths:
        if p.exists():
            return p
    return None

def tcp_reachable(host: str, ports, timeout=2):
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True, port
        except Exception:
            pass
    return False, None

def check_path(label, candidates):
    path = first_existing_path(candidates)
    if not path:
        return {
            "exists": False,
            "readable": False,
            "path": None,
            "label": label,
            "state": "ORANGE",
            "message": f"{label} is not mounted locally.",
        }

    if not os.access(path, os.R_OK):
        return {
            "exists": True,
            "readable": False,
            "path": str(path),
            "label": label,
            "state": "RED",
            "message": f"{label} exists locally but is not readable.",
        }

    return {
        "exists": True,
        "readable": True,
        "path": str(path),
        "label": label,
        "state": "GREEN",
        "message": f"{label} verified and readable locally.",
    }

def check_remote():
    remote_ok, remote_port = tcp_reachable(LIBRARY_REMOTE_HOST, LIBRARY_REMOTE_PORTS)
    return {
        "reachable": remote_ok,
        "port": remote_port,
        "host": LIBRARY_REMOTE_HOST,
    }

def check_header():
    if not HEADER_FILE.exists():
        return {"state": "NEXUS", "message": "Header file missing."}

    text = HEADER_FILE.read_text(errors="ignore")
    missing = [m for m in REQUIRED_MMS_MARKERS if m not in text]

    if len(missing) == len(REQUIRED_MMS_MARKERS):
        return {"state": "BLUE", "message": "Header visible; verification pending."}

    if missing:
        return {"state": "ORANGE", "message": "MMS security partially verified."}

    return {"state": "GREEN", "message": "MMS security verified."}

def check_bridge():
    bridge = read_json(BRIDGE_STATE_FILE)
    mesh = read_json(MESH_STATE_FILE)

    air_ok = False
    pro_ok = False
    mobile_present = False
    stale = False

    if bridge:
        if "targets" in bridge and isinstance(bridge["targets"], dict):
            air_ok = bool(bridge["targets"].get("air_local"))
            pro_ok = bool(bridge["targets"].get("pro_local"))
        else:
            air_ok = bool(bridge.get("air_ok", False))
            pro_ok = bool(bridge.get("pro_ok", False))

        ts = bridge.get("timestamp", 0)
        if isinstance(ts, int):
            stale = (int(time.time()) - ts) > 180

    if mesh:
        if isinstance(mesh.get("stable"), list):
            stable = set(mesh.get("stable", []))
            mobile_present = "iphone" in stable or "tablet" in stable
        else:
            nodes = mesh.get("nodes", {})
            if isinstance(nodes, dict):
                mobile_present = "iphone" in nodes or "tablet" in nodes

    if stale:
        return {"state": "GRAY", "message": "Bridge state is stale or indeterminate."}
    if air_ok and pro_ok and mobile_present:
        return {"state": "PURPLE", "message": "Bridge and mobile presence verified."}
    if air_ok and pro_ok:
        return {"state": "GREEN", "message": "Air and Pro bridge stable."}
    if air_ok or pro_ok:
        return {"state": "YELLOW", "message": "Only part of the bridge is visible."}
    return {"state": "BLUE", "message": "Node visible; bridge verification pending."}

def final_state():
    library = check_path("LAB_8TB/LIB_2TB", LIBRARY_CANDIDATES)
    workbench = check_path("LAB_8TB/WORKBENCH", WORKBENCH_CANDIDATES)
    remote = check_remote()
    header = check_header()
    bridge = check_bridge()

    if library["state"] == "RED" or workbench["state"] == "RED":
        color = "RED"
        message = "Library or Workbench exists locally but is not readable."
    elif header["state"] == "NEXUS" and not library["exists"] and not workbench["exists"] and not remote["reachable"]:
        color = "NEXUS"
        message = "No active node surface."
    elif header["state"] == "BLUE":
        color = "BLUE"
        message = "Node visible; verification pending."
    elif header["state"] == "ORANGE":
        color = "ORANGE"
        message = header["message"]
    elif library["state"] == "GREEN" and workbench["state"] == "GREEN" and header["state"] == "GREEN" and bridge["state"] == "PURPLE":
        color = "PURPLE"
        message = "Library, Workbench, MMS, and extended node presence verified."
    elif library["state"] == "GREEN" and workbench["state"] == "GREEN" and header["state"] == "GREEN":
        color = "GREEN"
        message = "Library, Workbench, and MMS security verified; stable."
    else:
        color = "ORANGE"
        if remote["reachable"]:
            message = "LAB_8TB reserve/workbench visible remotely but not mounted locally."
        else:
            message = "LAB_8TB reserve/workbench is not connected or reachable from drmarchandslab.com."

    return {
        "color": color,
        "icon": COLOR_MAP.get(color, " "),
        "message": message,
        "library": library,
        "workbench": workbench,
        "remote": remote,
        "header": header,
        "bridge": bridge,
        "timestamp": int(time.time()),
    }

def render():
    state = final_state()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"⚙︎  Nɛuro-Forge Engine™ : 🔐 MMS-768™ ⚛︎ Active {state['icon']}")
    print("Author  : J.K. Marchand • Cryptographic Publisher")
    print("Authority: © Design Orchard LLC")
    print("Runtime : 🔬 DrMarchand’s Lab⚛︎ratory™")
    print("Archive : 📚 DrMarchand’s ⚛︎ Library™")
    print("Workbench: 🪑 DrMarchand’s ⚛︎ Workbench™")
    print(f"WATCHER : {state['icon']} {state['color']}")
    print(f"Message : {state['message']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Library : {state['library']['message']}")
    print(f"Workbench: {state['workbench']['message']}")
    print(f"Remote  : {state['remote']['host']}")
    print(f"MMS     : {state['header']['message']}")
    print(f"Bridge  : {state['bridge']['message']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    render()
