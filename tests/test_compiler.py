import pytest
from pydantic import ValidationError

from intent_engineering import IntentCompiler, IntentSpec


def test_compiler_propagates_evidence_and_authority() -> None:
    spec = IntentSpec.model_validate(
        {
            "outcome": "Ship a correct contribution",
            "success_criteria": ["tests pass", "reviewer accepts"],
            "constraints": [{"rule": "do not change the public API", "kind": "hard"}],
            "priorities": [{"name": "correctness", "weight": 1.0}],
            "authority": [{"action": "publish", "decision": "approval_required"}],
        }
    )

    contract = IntentCompiler().compile(spec)

    assert contract.evidence_required == ["tests pass", "reviewer accepts"]
    assert "publish: approval_required" in contract.harness_rules
    assert any("do not change the public API" in rule for rule in contract.harness_rules)


def test_intent_requires_at_least_one_success_criterion() -> None:
    with pytest.raises(ValidationError):
        IntentSpec(outcome="Do something", success_criteria=[])


def test_named_entries_must_be_unique() -> None:
    with pytest.raises(ValidationError, match="priority names must be unique"):
        IntentSpec.model_validate(
            {
                "outcome": "Deliver",
                "success_criteria": ["accepted"],
                "priorities": [
                    {"name": "cost", "weight": 1},
                    {"name": "cost", "weight": 2},
                ],
            }
        )
