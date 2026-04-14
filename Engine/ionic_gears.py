# ⚛︎ Nɛuro-Forge Engine™ : Ionic Layer

from datetime import datetime

class IonicGear:
    def __init__(self, box_data):
        self.data = box_data
        self.ions = {}

    def compute_financials(self):
        subtotal = self.data.get("subtotal", 0)
        tax = self.data.get("tax", 0)
        labor = self.data.get("labor_total", 0) or 0

        self.ions["true_total_cost"] = subtotal + tax + labor
        return self

    def compute_margin(self):
        revenue = self.data.get("grandTotal", 0)
        cost = self.ions.get("true_total_cost", 0)

        self.ions["margin"] = revenue - cost if revenue else None
        self.ions["margin_ratio"] = cost / revenue if revenue else None
        return self

    def classify_job(self):
        if self.data.get("labor_hours") and self.data.get("print_projectFolder"):
            self.ions["job_state"] = "FULLY_PROCESSED"
        elif self.data.get("labor_hours"):
            self.ions["job_state"] = "LABOR_ONLY"
        elif self.data.get("print_projectFolder"):
            self.ions["job_state"] = "PRINT_ONLY"
        else:
            self.ions["job_state"] = "FINANCIAL_ONLY"
        return self

    def emit(self):
        return {**self.data, **self.ions}


def run_ionic_layer(box_data):
    return (
        IonicGear(box_data)
        .compute_financials()
        .compute_margin()
        .classify_job()
        .emit()
    )


if __name__ == "__main__":
    sample = {
        "subtotal": 450,
        "tax": 31.5,
        "grandTotal": 450,
        "labor_total": 200,
        "labor_hours": 4,
        "print_projectFolder": "drive/x"
    }

    print(run_ionic_layer(sample))
