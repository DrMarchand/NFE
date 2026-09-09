import json
import os
from ScoringGear import ScoringGear


def required_path(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required private configuration is missing: {name}")
    return os.path.expanduser(value)


def run_intake():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("DrMarchand’s ⚙︎ Nɛuro-Forge Engine™ : HubSpot Semantic Intake")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    name = input("Agency/Partner Name: ")
    acronym = input("Company Acronym: ").strip().upper()

    company_id = input("HubSpot Company Short ID: ").strip()
    partner_id_suffix = input("HubSpot Partner ID: ").strip()

    system_id = f"{acronym}-{company_id}.{partner_id_suffix}"
    print(f"🔗 [LINKED] Core Entity Forged: {system_id}")

    volume = input("Client Volume (High/Medium/Low): ").strip().capitalize()

    while True:
        try:
            match = int(input("Execution Match Score (0-100): "))
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
    os.makedirs(nodes_root, exist_ok=True)
    save_path = os.path.join(nodes_root, f"{system_id}.json")

    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)

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
