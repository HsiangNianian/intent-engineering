"""Typed contracts for expressing intent without hiding value choices in prompts."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Constraint(BaseModel):
    """A boundary that an execution system must preserve."""

    rule: str = Field(min_length=1)
    kind: Literal["hard", "soft"] = "hard"
    rationale: str | None = None


class Priority(BaseModel):
    """A named optimization objective and its relative importance."""

    name: str = Field(min_length=1)
    weight: float = Field(default=1.0, gt=0)


class AuthorityRule(BaseModel):
    """A consequential action and the authority required to perform it."""

    action: str = Field(min_length=1)
    decision: Literal["autonomous", "approval_required", "forbidden"]


class IntentSpec(BaseModel):
    """An explicit, reviewable statement of what the system owes its user."""

    outcome: str = Field(min_length=1)
    success_criteria: list[str] = Field(min_length=1)
    constraints: list[Constraint] = Field(default_factory=list)
    priorities: list[Priority] = Field(default_factory=list)
    authority: list[AuthorityRule] = Field(default_factory=list)
    ambiguity_policy: Literal["ask", "conservative", "fail"] = "ask"

    @model_validator(mode="after")
    def unique_named_entries(self) -> "IntentSpec":
        priority_names = [priority.name for priority in self.priorities]
        authority_actions = [rule.action for rule in self.authority]
        if len(priority_names) != len(set(priority_names)):
            raise ValueError("priority names must be unique")
        if len(authority_actions) != len(set(authority_actions)):
            raise ValueError("authority actions must be unique")
        return self


class ExecutionContract(BaseModel):
    """Deterministic obligations emitted for the lower engineering layers."""

    outcome: str
    prompt_requirements: list[str]
    context_requirements: list[str]
    harness_rules: list[str]
    loop_exit_conditions: list[str]
    graph_requirements: list[str]
    emergence_boundaries: list[str]
    evidence_required: list[str]
