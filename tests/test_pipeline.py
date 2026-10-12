import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.requirements_parser import translate_requirements, parse_requirement, BUSINESS_REQUIREMENTS
from src.simulate_data import simulate
from src.rule_engine import run_rules, overall_accuracy


@pytest.fixture(scope="module")
def rules():
    return translate_requirements()


@pytest.fixture(scope="module")
def df():
    return simulate()


def test_exactly_45_requirements_and_rules(rules):
    assert len(BUSINESS_REQUIREMENTS) == 45
    assert len(rules) == 45


def test_range_requirement_parses_correctly():
    rule = parse_requirement("Patient age must be between 0 and 120")
    assert rule["rule_type"] == "range"
    assert rule["params"] == {"min": 0.0, "max": 120.0}


def test_code_list_requirement_parses_correctly():
    rule = parse_requirement("Insurance type must be one of Commercial, Medicare")
    assert rule["rule_type"] == "code_list"
    assert rule["params"]["allowed"] == ["Commercial", "Medicare"]


def test_unparseable_requirement_raises():
    with pytest.raises(ValueError):
        parse_requirement("This is not a valid requirement sentence")


def test_all_rule_fields_exist_in_simulated_data(rules, df):
    missing_fields = [r["field"] for r in rules if r["field"] not in df.columns]
    assert missing_fields == []


def test_injected_defects_are_detected(rules, df):
    results = run_rules(df, rules)
    assert any(r["pass_rate_pct"] < 100 for r in results)


def test_overall_accuracy_in_realistic_band(rules, df):
    results = run_rules(df, rules)
    accuracy = overall_accuracy(results)
    assert 95.0 <= accuracy["overall_accuracy_pct"] <= 100.0
