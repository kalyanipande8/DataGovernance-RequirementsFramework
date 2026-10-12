"""Simulate a healthcare dataset whose fields correspond exactly to the
45 translated technical rules, with realistic injected defects, so the
rule engine has something genuine to validate."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_RECORDS = 600
SEED = 149

FIELD_SPECS = {
    "patient_age": ("range", 0, 95), "medical_record_number": ("id",),
    "patient_sex": ("cat", ["M", "F", "U"]),
    "insurance_type": ("cat", ["Commercial", "Medicare", "Medicaid", "Uninsured"]),
    "zip_code": ("zip",), "visit_date": ("date",),
    "systolic_blood_pressure": ("range", 90, 180), "diastolic_blood_pressure": ("range", 60, 110),
    "heart_rate": ("range", 50, 110), "temperature_fahrenheit": ("range", 97, 101),
    "encounter_id": ("id",), "provider_npi": ("npi",),
    "weight_kg": ("range", 40, 150), "height_cm": ("range", 140, 200), "bmi": ("range", 15, 45),
    "glucose_mg_dl": ("range", 60, 300), "hba1c_percent": ("range", 4, 14),
    "creatinine_mg_dl": ("range", 0.4, 5), "sodium_meq_l": ("range", 125, 150),
    "potassium_meq_l": ("range", 2.5, 6), "hemoglobin_g_dl": ("range", 7, 18),
    "white_blood_cell_count": ("range", 2, 20), "platelet_count": ("range", 50, 500),
    "oxygen_saturation_percent": ("range", 80, 100), "respiratory_rate": ("range", 10, 30),
    "claim_id": ("id",), "payer_id": ("id",), "facility_id": ("id",),
    "diagnosis_code": ("id",), "procedure_code": ("id",),
    "phone_number": ("phone",), "email_address": ("email",), "state_code": ("state",),
    "npi_secondary": ("npi",), "language_preference": ("cat", ["English", "Spanish", "Other"]),
    "admission_date": ("date",), "discharge_date": ("date",),
}
CODE_LIST_FIELDS = {
    "gender_identity": ["Male", "Female", "Non-binary", "Unknown"],
    "marital_status": ["Single", "Married", "Divorced", "Widowed", "Unknown"],
    "race": ["White", "Black", "Asian", "Other", "Unknown"],
    "ethnicity": ["Hispanic", "Not Hispanic", "Unknown"],
    "admission_source": ["Emergency", "Referral", "Transfer", "Unknown"],
    "discharge_disposition": ["Home", "SNF", "Hospice", "Expired", "Unknown"],
    "pregnancy_status": ["Yes", "No", "Unknown"],
    "smoking_status": ["Current", "Former", "Never", "Unknown"],
}


def simulate(n: int = N_RECORDS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    data = {}

    for field, spec in FIELD_SPECS.items():
        kind = spec[0]
        if kind == "range":
            lo, hi = spec[1], spec[2]
            data[field] = np.round(rng.uniform(lo, hi, n), 1)
        elif kind == "id":
            data[field] = [f"ID-{i:06d}" for i in range(n)]
        elif kind == "cat":
            data[field] = rng.choice(spec[1], n)
        elif kind == "zip":
            data[field] = [f"{rng.integers(10000, 99999)}" for _ in range(n)]
        elif kind == "date":
            data[field] = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 300, n), unit="D")
        elif kind == "npi":
            data[field] = [f"{rng.integers(10**9, 10**10)}" for _ in range(n)]
        elif kind == "phone":
            data[field] = [f"{rng.integers(10**9, 10**10)}" for _ in range(n)]
        elif kind == "email":
            data[field] = [f"patient{i}@example.com" for i in range(n)]
        elif kind == "state":
            data[field] = rng.choice(["NY", "CA", "TX", "FL"], n)

    for field, levels in CODE_LIST_FIELDS.items():
        data[field] = rng.choice(levels, n)

    df = pd.DataFrame(data)

    # realistic injected defects, ~0.3-1% per affected field
    for field in ["patient_age", "systolic_blood_pressure", "glucose_mg_dl", "bmi"]:
        idx = rng.choice(df.index, size=max(1, int(n * 0.005)), replace=False)
        df.loc[idx, field] = -999
    for field in ["medical_record_number", "encounter_id", "diagnosis_code"]:
        idx = rng.choice(df.index, size=max(1, int(n * 0.003)), replace=False)
        df.loc[idx, field] = None
    idx = rng.choice(df.index, size=max(1, int(n * 0.004)), replace=False)
    df.loc[idx, "insurance_type"] = "Unknown Plan Type"
    idx = rng.choice(df.index, size=max(1, int(n * 0.004)), replace=False)
    df.loc[idx, "zip_code"] = "ABCDE"

    return df


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
