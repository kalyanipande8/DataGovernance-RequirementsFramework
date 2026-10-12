"""End-to-end: translate 45 business requirements into technical rules,
simulate data, and run the generic rule engine."""
import json
import os

from src.requirements_parser import translate_requirements, BUSINESS_REQUIREMENTS
from src.simulate_data import simulate
from src.rule_engine import run_rules, overall_accuracy

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print(f"=== Translating {len(BUSINESS_REQUIREMENTS)} business requirements to technical rules ===")
rules = translate_requirements()
for r in rules[:5]:
    print(r)

print("\n=== Simulating healthcare dataset ===")
df = simulate()
df.to_csv("data/healthcare_records.csv", index=False)
print(df.shape)

print("\n=== Running the generic rule engine ===")
results = run_rules(df, rules)
import pandas as pd
results_df = pd.DataFrame(results)
results_df.to_csv("results/rule_results.csv", index=False)
print(results_df[results_df["pass_rate_pct"] < 100][["rule_id", "field", "pass_rate_pct"]])

accuracy = overall_accuracy(results)
print(accuracy)

summary = {
    "n_business_requirements": len(BUSINESS_REQUIREMENTS),
    "n_technical_rules_translated": len(rules),
    "n_records": len(df),
    **accuracy,
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
