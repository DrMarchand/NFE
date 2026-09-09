import json
import os


class ScoringGear:
    def __init__(self, partner_file_path):
        with open(partner_file_path, "r") as f:
            self.partner = json.load(f)
        self.score = 50

    def calculate_score(self):
        print(f"⚙︎ [SCORING GEAR] Analyzing Partner: {self.partner.get('display_name')}")

        caps = self.partner.get("capabilities", {})
        if caps.get("client_volume") == "High":
            self.score += 20
        if caps.get("client_volume") == "Medium":
            self.score += 10

        fit = self.partner.get("execution_fit", {})
        match = fit.get("match_score", 50)
        self.score += match * 0.2

        risk = self.partner.get("risk_profile", {})
        if risk.get("payment_delay_risk") == "High":
            self.score -= 40
        if risk.get("payment_delay_risk") == "Medium":
            self.score -= 15

        flags = risk.get("red_flags", [])
        for flag in flags:
            print(f"   ⚠️ WARNING: Red flag detected -> [{flag.upper()}] (-15 pts)")
            self.score -= 15

        self.score = max(0, min(100, int(self.score)))
        return self.score

    def verdict(self):
        if self.score >= 85:
            return "🟩 TIER 1: STRATEGIC PARTNER (Prioritize Flow)"
        if self.score >= 65:
            return "🟨 TIER 2: ACTIVE (Proceed with Standard Contracts)"
        if self.score >= 40:
            return "🟧 TIER 3: PROBATION (Strict Scope, Upfront Payments Only)"
        return "🟥 BLOCK: DO NOT ENGAGE WITHOUT HUMAN REVIEW"


if __name__ == "__main__":
    filepath = os.environ.get("NFE_SCORING_SAMPLE", "").strip()
    if not filepath:
        raise RuntimeError("Set NFE_SCORING_SAMPLE to an authorized local sample file")

    filepath = os.path.expanduser(filepath)
    if not os.path.exists(filepath):
        raise FileNotFoundError("Configured NFE_SCORING_SAMPLE does not exist")

    gear = ScoringGear(filepath)
    final_score = gear.calculate_score()

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 PARTNER LAB-FIT SCORE : {final_score} / 100")
    print(f"⚖️ VERDICT               : {gear.verdict()}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
