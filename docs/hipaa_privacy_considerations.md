# HIPAA & Privacy Considerations

**Status: an authored compliance analysis applied to this project's
simulated data schema — not a real covered-entity's compliance
attestation.**

## HIPAA Safe Harbor — the 18 identifiers
The HIPAA Privacy Rule's Safe Harbor method (45 CFR §164.514(b)(2)) names
18 categories of identifiers that must be removed for data to be
considered de-identified. Applied to this project's 45-field schema:

| # | Safe Harbor identifier category | Present in this schema? |
|---|---|---|
| 1 | Names | No |
| 2 | Geographic subdivisions smaller than state | **Yes** — `zip_code` |
| 3 | Dates (except year) directly related to an individual | **Yes** — `visit_date`, `admission_date`, `discharge_date` |
| 4 | Telephone numbers | **Yes** — `phone_number` |
| 5 | Fax numbers | No |
| 6 | Email addresses | **Yes** — `email_address` |
| 7 | Social security numbers | No |
| 8 | Medical record numbers | **Yes** — `medical_record_number` |
| 9 | Health plan beneficiary numbers | **Yes** — `payer_id` (plan-adjacent) |
| 10 | Account numbers | No |
| 11 | Certificate/license numbers | **Yes** — `provider_npi`, `npi_secondary` |
| 12 | Vehicle identifiers | No |
| 13 | Device identifiers | No |
| 14 | URLs | No |
| 15 | IP addresses | No |
| 16 | Biometric identifiers | No |
| 17 | Full-face photos | No |
| 18 | Any other unique identifying number/code | **Yes** — `encounter_id`, `claim_id`, `facility_id` |

**7 of 18 Safe Harbor categories are present** in this schema — meaning
this dataset, as structured, would need de-identification (removal or
generalization of the flagged fields, e.g. ZIP truncated to 3 digits,
dates shifted to year-only) before it could be shared or used outside a
covered entity's treatment/payment/operations purposes under HIPAA.

## Minimum necessary & access controls
- `medical_record_number`, `provider_npi`, and `encounter_id` should be
  access-restricted to roles with a treatment/operations need, not broadly
  queryable.
- `zip_code`, `phone_number`, and `email_address` should be masked or
  generalized in any analytics/reporting context that doesn't require
  patient-level contact information.

## Honest disclosure
This is a schema-level Safe Harbor identifier analysis for this project's
simulated field list — it is not a real HIPAA risk assessment, Expert
Determination analysis, or covered-entity compliance attestation.
