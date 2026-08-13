"""Compile an :class:`IntentSpec` into obligations for the execution stack."""

from intent_engineering.models import ExecutionContract, IntentSpec


class IntentCompiler:
    """A deliberately deterministic first compiler pass.

    Language models may extract a draft ``IntentSpec`` from natural language, but the
    transformation from an approved specification to an execution contract stays inspectable.
    """

    def compile(self, spec: IntentSpec) -> ExecutionContract:
        hard_constraints = [item.rule for item in spec.constraints if item.kind == "hard"]
        soft_constraints = [item.rule for item in spec.constraints if item.kind == "soft"]
        authority = [f"{rule.action}: {rule.decision}" for rule in spec.authority]
        priorities = [f"{item.name} (weight={item.weight:g})" for item in spec.priorities]

        return ExecutionContract(
            outcome=spec.outcome,
            prompt_requirements=[
                f"State the owed outcome: {spec.outcome}",
                *[f"Preserve hard constraint: {rule}" for rule in hard_constraints],
            ],
            context_requirements=[
                "Retain the approved intent specification and its provenance.",
                *[f"Expose optimization priority: {priority}" for priority in priorities],
            ],
            harness_rules=[
                *authority,
                *[f"Enforce hard constraint: {rule}" for rule in hard_constraints],
            ],
            loop_exit_conditions=[
                *[f"Provide evidence for: {criterion}" for criterion in spec.success_criteria],
                f"Resolve ambiguity using policy: {spec.ambiguity_policy}",
            ],
            graph_requirements=[
                "Assign an accountable owner for every success criterion.",
                "Route independent verification separately from production work.",
                *[f"Treat as a trade-off, not a hard gate: {rule}" for rule in soft_constraints],
            ],
            emergence_boundaries=[
                "Topology changes may not weaken hard constraints or authority rules.",
                "Every mutation must be attributable, reversible, and evaluated.",
            ],
            evidence_required=list(spec.success_criteria),
        )
