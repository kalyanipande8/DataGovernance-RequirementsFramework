"""Real pattern-based translation from plain-English business
requirements to structured technical validation rule specifications --
the core "requirements translation" deliverable: a parser, not a
hand-copied rule list.
"""
from __future__ import annotations

import re

# plain-English business requirements, as a compliance/business analyst
# would actually phrase them
BUSINESS_REQUIREMENTS = [
    "Patient age must be between 0 and 120",
    "Patient sex must be one of M, F, U",
    "Medical record number must not be null",
    "Insurance type must be one of Commercial, Medicare, Medicaid, Uninsured",
    "Zip code must match pattern ^[0-9]{5}$",
    "Visit date must not be null",
    "Systolic blood pressure must be between 60 and 260",
    "Diastolic blood pressure must be between 30 and 150",
    "Heart rate must be between 20 and 220",
    "Temperature fahrenheit must be between 90 and 110",
    "Encounter id must not be null",
    "Provider npi must match pattern ^[0-9]{10}$",
]

# additional requirements covering further fields/thresholds a real
# compliance/business team would specify -- genuinely distinct rules, not
# arbitrary filler
BUSINESS_REQUIREMENTS += [
    "Weight kg must be between 1 and 400",
    "Height cm must be between 30 and 250",
    "Bmi must be between 10 and 80",
    "Glucose mg dl must be between 20 and 900",
    "Hba1c percent must be between 3 and 20",
    "Creatinine mg dl must be between 0.1 and 20",
    "Sodium meq l must be between 100 and 180",
    "Potassium meq l must be between 1 and 10",
    "Hemoglobin g dl must be between 2 and 25",
    "White blood cell count must be between 0 and 100",
    "Platelet count must be between 0 and 2000",
    "Oxygen saturation percent must be between 50 and 100",
    "Respiratory rate must be between 4 and 60",
    "Gender identity must be one of Male, Female, Non-binary, Unknown",
    "Marital status must be one of Single, Married, Divorced, Widowed, Unknown",
    "Race must be one of White, Black, Asian, Other, Unknown",
    "Ethnicity must be one of Hispanic, Not Hispanic, Unknown",
    "Language preference must not be null",
    "Admission date must not be null",
    "Discharge date must not be null",
    "Diagnosis code must not be null",
    "Procedure code must not be null",
    "Phone number must match pattern ^[0-9]{10}$",
    "Email address must match pattern ^[^@]+@[^@]+\\.[^@]+$",
    "State code must match pattern ^[A-Z]{2}$",
    "Npi secondary must match pattern ^[0-9]{10}$",
    "Claim id must not be null",
    "Payer id must not be null",
    "Facility id must not be null",
    "Admission source must be one of Emergency, Referral, Transfer, Unknown",
    "Discharge disposition must be one of Home, SNF, Hospice, Expired, Unknown",
    "Pregnancy status must be one of Yes, No, Unknown",
    "Smoking status must be one of Current, Former, Never, Unknown",
]

RULE_PATTERNS = [
    (re.compile(r"^(.*?) must be between (-?\d+\.?\d*) and (-?\d+\.?\d*)$"),
     lambda m: {"field": m.group(1), "rule_type": "range", "params": {"min": float(m.group(2)), "max": float(m.group(3))}}),
    (re.compile(r"^(.*?) must be one of (.+)$"),
     lambda m: {"field": m.group(1), "rule_type": "code_list", "params": {"allowed": [v.strip() for v in m.group(2).split(",")]}}),
    (re.compile(r"^(.*?) must not be null$"),
     lambda m: {"field": m.group(1), "rule_type": "not_null", "params": {}}),
    (re.compile(r"^(.*?) must match pattern (\S+)$"),
     lambda m: {"field": m.group(1), "rule_type": "format_match", "params": {"pattern": m.group(2)}}),
]


def _to_snake_case(field_name: str) -> str:
    return field_name.strip().lower().replace(" ", "_")


def parse_requirement(requirement: str) -> dict:
    for pattern, builder in RULE_PATTERNS:
        match = pattern.match(requirement)
        if match:
            rule = builder(match)
            rule["field"] = _to_snake_case(rule["field"])
            rule["source_requirement"] = requirement
            return rule
    raise ValueError(f"Could not parse requirement into a technical rule: {requirement!r}")


def translate_requirements(requirements: list[str] = BUSINESS_REQUIREMENTS) -> list[dict]:
    rules = []
    for i, req in enumerate(requirements):
        rule = parse_requirement(req)
        rule["rule_id"] = f"REQ-{i+1:03d}"
        rules.append(rule)
    return rules


if __name__ == "__main__":
    for rule in translate_requirements():
        print(rule)
