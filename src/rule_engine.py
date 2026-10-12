"""A generic rule engine executing the 45 translated technical
specifications against the simulated data -- one dispatch table, not 45
bespoke functions, so a new business requirement only needs a new
specification row, not new code."""
from __future__ import annotations

import re

import pandas as pd


def _not_null(df, field, params):
    return df[field].notna()


def _range(df, field, params):
    non_null = df[field].notna()
    in_range = df[field].between(params["min"], params["max"])
    return ~non_null | in_range  # missing values aren't a range violation here (separate not_null rule covers that)


def _code_list(df, field, params):
    non_null = df[field].notna()
    in_list = df[field].isin(params["allowed"])
    return ~non_null | in_list


def _format_match(df, field, params):
    pattern = re.compile(params["pattern"])
    non_null = df[field].notna()
    matches = df[field].astype(str).apply(lambda v: bool(pattern.match(v)))
    return ~non_null | matches


DISPATCH = {"not_null": _not_null, "range": _range, "code_list": _code_list, "format_match": _format_match}


def run_rules(df: pd.DataFrame, rules: list[dict]) -> list[dict]:
    results = []
    for rule in rules:
        field = rule["field"]
        if field not in df.columns:
            results.append({**rule, "n_total": len(df), "n_pass": 0, "pass_rate_pct": 0.0})
            continue
        handler = DISPATCH[rule["rule_type"]]
        pass_mask = handler(df, field, rule["params"])
        results.append({
            **rule, "n_total": len(df), "n_pass": int(pass_mask.sum()),
            "pass_rate_pct": round(100 * pass_mask.mean(), 3),
        })
    return results


def overall_accuracy(results: list[dict]) -> dict:
    total = sum(r["n_total"] for r in results)
    passed = sum(r["n_pass"] for r in results)
    return {"n_rules": len(results), "total_checks": total,
            "overall_accuracy_pct": round(100 * passed / total, 4)}


if __name__ == "__main__":
    from .simulate_data import simulate
    from .requirements_parser import translate_requirements

    df = simulate()
    rules = translate_requirements()
    results = run_rules(df, rules)
    for r in results:
        if r["pass_rate_pct"] < 100:
            print(r["rule_id"], r["field"], r["pass_rate_pct"])
    print(overall_accuracy(results))
