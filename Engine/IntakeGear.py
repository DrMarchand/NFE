import json
import os
import re
from pathlib import Path
from ScoringGear import ScoringGear


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


# Keep IDs textual: HubSpot IDs may exceed integer precision or have leading zeros.
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*", re.ASCII)
_SYSTEM_ID = re.compile(r"[A-Z0-9][A-Z0-9_-]*-[A-Za-z0-9][A-Za-z0-9_-]*\.[A-Za-z0-9][A-Za-z0-9_-]*", re.ASCII)


def identifier(value, label):
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text")
    value = value.strip()
    if not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label} must start with an ASCII letter or digit and contain only letters, digits, _ or -")
    return value


def build_system_id(acronym, company_id, partner_id):
    acronym = identifier(acronym, "Company acronym").upper()
    company_id = identifier(company_id, "Company ID")
    partner_id = identifier(partner_id, "Partner ID")
    system_id = f"{acronym}-{company_id}.{partner_id}"
    node_filename(system_id)
    return system_id, acronym, company_id, partner_id


def node_filename(system_id):
    # Reject rather than sanitize: changing bytes could alias another record.
    if not isinstance(system_id, str) or not _SYSTEM_ID.fullmatch(system_id):
        raise ValueError("Invalid system identifier")
    filename = f"{system_id}.json"
    if len(filename.encode("ascii")) > 255:
        raise ValueError("Node filename exceeds 255 bytes")
    return filename


def match_score(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,3}", value.strip()):
        raise ValueError("Score must be a whole number between 0 and 100")
    score = int(value.strip())
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100")
    return score


def open_nodes_root(root):
    """Create/open a trusted root without following any symlink component.

    Descriptor-relative traversal pins each parent while opening its child.
    Fail closed on platforms lacking the required POSIX primitives.
    """
    if (not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY")
            or os.open not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd):
        raise RuntimeError("Intake requires POSIX no-follow directory operations")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(root.anchor, flags)
    try:
        for part in root.parts[1:]:
            try:
                os.mkdir(part, mode=0o700, dir_fd=fd)
            except FileExistsError:
                pass
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def save_node(nodes_root, data):
    """Create a new node only; never replace an existing file or follow a link."""
    filename = node_filename(data["system_id"])
    # Serialize before creating directories, including malformed-record failures.
    payload = json.dumps(data, indent=2).encode("utf-8")
    root = Path(os.path.abspath(os.path.expanduser(nodes_root)))
    destination = root / filename
    if destination.resolve().parent != root.resolve():
        raise ValueError("Node destination escapes the configured root")
    root_fd = open_nodes_root(root)
    try:
        fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=root_fd)
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
    finally:
        os.close(root_fd)
    return str(destination)


def run_intake():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("DrMarchand’s ⚙︎ Nɛuro-Forge Engine : HubSpot Semantic Intake")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    name = input("Agency/Partner Name: ")
    acronym = input("Company Acronym: ")

    company_id = input("HubSpot Company Short ID: ").strip()
    partner_id_suffix = input("HubSpot Partner ID: ").strip()

    system_id, acronym, company_id, partner_id_suffix = build_system_id(
        acronym, company_id, partner_id_suffix
    )
    print(f"🔗 [LINKED] Core Entity Forged: {system_id}")

    volume = input("Client Volume (High/Medium/Low): ").strip().capitalize()

    while True:
        try:
            match = match_score(input("Execution Match Score (0-100): "))
            break
        except ValueError:
            print("Please enter a number between 0 and 100.")

    pay_risk = input("Payment Delay Risk (High/Medium/Low): ").strip().capitalize()
    flags_input = input("Red Flags (comma separated, or leave blank): ")
    flags = [f.strip().lower() for f in flags_input.split(",")] if flags_input.strip() else []

    data = {
        "system_id": system_id,
        "hubspot": {
            "company_id": company_id,
            "partner_id": partner_id_suffix,
            "acronym": acronym,
        },
        "display_name": name,
        "type": "Agency",
        "status": "Lead",
        "capabilities": {
            "client_volume": volume,
            "urgency_level": "TBD",
        },
        "execution_fit": {
            "match_score": match,
            "recommended_engagement_model": "TBD",
        },
        "risk_profile": {
            "reliability_score": 5,
            "payment_delay_risk": pay_risk,
            "red_flags": flags,
        },
    }

    nodes_root = required_path("NFE_NODES_ROOT")
    save_path = save_node(nodes_root, data)

    print(f"\n🟩 INTAKE COMPLETE: {name} injected as {system_id}")
    print("\n⚙︎ [AUTO-LINK] Firing ScoringGear...")
    gear = ScoringGear(save_path)
    final_score = gear.calculate_score()

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 PARTNER LAB-FIT SCORE : {final_score} / 100")
    print(f"⚖️ VERDICT               : {gear.verdict()}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


if __name__ == "__main__":
    run_intake()
