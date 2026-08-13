# Intent Engineering — a.k.a. Wish Engineering

> **许愿工程:** make a wish, then require the machine to say what it thinks the wish means,
> what it may do, what would count as granted, and when it must ask again.

Intent Engineering studies how a human wish becomes an explicit, reviewable, and
machine-operable contract for an agent system. The nickname **Wish Engineering** is
deliberately theatrical. The implementation is deliberately not.

It is not wishful prompting and it is not permission for a model to decide what a person
"really meant." The working artifact is an **intent specification**: an outcome, success
criteria, constraints, priorities, authority boundaries, ambiguity policy, and required
evidence. An intent compiler then projects that specification into obligations for the
execution stack.

> Status: **early research scaffold**. The schema and compiler are deliberately small and
> unstable. Do not use them as a production authorization system.

## The joke, and the serious part

**Wish Engineering** is partly a joke about the endless escalation of engineering labels:
prompt engineering, context engineering, harness engineering, loop engineering, graph
engineering—and finally, apparently, just make a wish.

The joke lands because that is how agent systems are often sold. The serious problem begins
immediately afterward: human wishes are incomplete, contradictory, value-laden, and rarely
executable as written. A capable agent can follow every local instruction and still optimize
the wrong outcome, cross an authority boundary, or declare victory without evidence.

This repository treats a wish as **untrusted source material**, not as an executable command.
Before work begins, it must become a contract that exposes:

- the outcome being requested;
- the evidence that would prove the wish was granted;
- hard constraints and negotiable trade-offs;
- actions the system may take autonomously;
- actions that require approval or remain forbidden;
- ambiguities that must be returned to the human instead of silently resolved.

## Why this repository exists

Agent failures increasingly occur after a model has correctly completed its immediate task:
the output is technically valid but does not achieve the desired outcome, a proxy metric is
optimized at the expense of the real goal, or a consequential action is taken without the
right authority. Better prompts alone do not resolve those failures.

This repository makes the missing decisions inspectable before execution:

- What outcome does the system owe?
- What evidence counts as success?
- Which constraints are inviolable and which are trade-offs?
- What may the system do autonomously?
- When must it ask, stop, or escalate?
- May an adaptive topology change this contract? (No.)

## Place in the Agent Engineering Stack

| Layer | Engineering object | Question |
| --- | --- | --- |
| [Prompt Engineering](https://github.com/HsiangNianian/prompt-engineering) | instructions | How should the model be asked? |
| [Context Engineering](https://github.com/HsiangNianian/context-engineering) | information environment | What should this step know, remember, and forget? |
| [Harness Engineering](https://github.com/HsiangNianian/harness-engineering) | runtime and authority | What can the agent do, and how is execution contained? |
| [Loop Engineering](https://github.com/HsiangNianian/loop-engineering) | feedback cycle | How does one agent continue, verify, recover, and stop? |
| [Graph Engineering](https://github.com/HsiangNianian/graph-engineering) | explicit organization | How do multiple loops coordinate and share state? |
| [Emergence Engineering](https://github.com/HsiangNianian/emergence-engineering) | adaptive organization | How may roles and topology change under bounded feedback? |
| **Intent Engineering** | goals and governance | What must be achieved, under which constraints and authority? |

Intent is a control plane, not merely the final historical step. It constrains every layer,
including any topology mutation performed by an emergent system.

## Wish Engineering is not Wishlist Engineering

This repository owns **one wish becoming one approved intent contract**.
[Wishlist Engineering](https://github.com/HsiangNianian/wishlist-engineering) is a separate
project with a different job: maintaining a portfolio of wishes and coordinating the complete
Agent Engineering Stack to turn them into evidence-backed outcomes.

```text
Wishlist Engineering
    │
    ├── accepts, clarifies, prioritizes, pauses, and revises wishes
    │
    ├── Intent Engineering      compiles each wish into a contract
    ├── Graph Engineering       organizes the work
    ├── Loop Engineering        drives each worker toward evidence
    ├── Harness Engineering     enforces execution and authority boundaries
    ├── Context Engineering     assembles what each decision needs to know
    ├── Prompt Engineering      renders model-facing instructions
    └── Emergence Engineering   adapts organization within the contract
                                 │
                                 ▼
                    evidence, outcome, or clarification
```

That repository is intended to become a **living system above the stack**, not an eighth synonym
beside it. It should integrate the seven projects through versioned contracts and adapters,
reuse their knowledge and implementations, and preserve their boundaries. It should not copy
their README content into one large prompt or hide their responsibilities inside a monolithic
orchestrator.

The distinction is intentional:

- **Wish Engineering:** “What does this wish actually commit the system to?”
- **Wishlist Engineering:** “Which wishes exist, which should run now, and how does the whole
  system deliver them over time?”

## What belongs here

- typed intent and execution-contract schemas;
- ambiguity detection and clarification protocols;
- deterministic compilation into lower-layer obligations;
- outcome, constraint, authority, and evidence evaluation;
- intent versioning, provenance, conflict handling, and change control;
- adapters that hand contracts to graph runtimes.

## Non-goals

- optimizing prompt wording;
- deciding which documents fit in a context window;
- implementing tool sandboxes or retries;
- serving as a general multi-agent orchestrator;
- allowing an LLM to invent goals, permissions, or organizational values;
- claiming that all human intent can be inferred from a short request.

## Current prototype

The package currently provides:

- `IntentSpec`, a Pydantic model for outcome, evidence, constraints, priorities, and authority;
- `IntentCompiler`, a deterministic projection into obligations for the other six layers;
- an optional OpenAI-backed extractor that creates a **draft** specification;
- a CLI that can compile an approved JSON specification without network access.

The OpenAI integration follows the official Python SDK's Responses API. Pydantic Settings
loads local configuration from `.env`; `.env` is ignored by Git.

## Quickstart

Requirements: Python 3.12+, [`uv`](https://docs.astral.sh/uv/), and optionally an OpenAI API
key for natural-language extraction.

```bash
uv sync
uv run intent-engineering --spec examples/intent.example.json
```

To extract a draft from natural language:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY.
uv run intent-engineering --goal "Ship a correct contribution without changing the public API"
```

Review the extracted specification before treating it as approved intent. Never commit
`.env` or an API key.

## Configuration

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | for `--goal` | none | OpenAI API authentication |
| `OPENAI_MODEL` | no | `gpt-5.6` | model used only for draft extraction |
| `OPENAI_BASEURL` | no | OpenAI SDK default | custom Responses-compatible API base URL |

`--spec` compilation is deterministic and does not call an LLM.
When `OPENAI_BASEURL` is unset or blank, the OpenAI SDK uses its default endpoint. A custom
endpoint must implement the Responses API used by the extractor.

## Architecture

```text
natural-language goal
        │
        ▼
OpenAIIntentExtractor ── draft IntentSpec ── human review/approval
                                               │
approved JSON IntentSpec ──────────────────────┘
        │
        ▼
IntentCompiler
        │
        ├── prompt requirements
        ├── context requirements
        ├── harness and authority rules
        ├── loop exit conditions
        ├── graph requirements
        ├── emergence mutation boundaries
        └── required evidence
```

The compiler is deterministic by design. Probabilistic extraction is kept on the untrusted
side of the approval boundary.

## Repository tree

```text
.
├── docs/
│   ├── concepts/       # stable vocabulary and invariants
│   └── roadmap/        # durable phase-level roadmap
├── evals/              # evaluation suites and result conventions
├── examples/           # approved IntentSpec examples
├── experiments/        # reproducible extraction and compiler studies
├── schemas/            # future versioned JSON Schema artifacts
├── src/intent_engineering/
│   ├── cli.py          # local CLI
│   ├── compiler.py     # deterministic compiler
│   ├── config.py       # Pydantic .env settings
│   ├── extractor.py    # OpenAI Responses API adapter
│   └── models.py       # intent and execution contracts
└── tests/              # unit tests; no live API calls
```

The documentation and research directories are intentional roadmap placeholders. Each is
tracked now so future work has an explicit home rather than accumulating in the package.

## Roadmap

### Phase 1 — Contract

- stabilize intent vocabulary and schema versioning;
- distinguish missing information from genuine value conflict;
- add machine-readable provenance and change history.

### Phase 2 — Compiler

- define lower-layer intermediate representations;
- add diagnostics for unsatisfiable or conflicting constraints;
- generate reviewable execution plans without granting new authority.

### Phase 3 — Evaluation

- build held-out ambiguity and proxy-gaming cases;
- measure constraint propagation and escalation correctness;
- compare human-authored, model-drafted, and jointly reviewed specifications.

### Phase 4 — Integration

- add framework-neutral graph and harness adapters;
- propagate intent changes to active runs safely;
- preserve an audit trail from purpose to evidence.

GitHub milestones and issues track the actionable slices of this roadmap.

## Development

```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

Tests must mock model boundaries. Live evaluation runs belong under `experiments/` and must
record the model and configuration used.

## Design principles

1. **Intent is explicit.** Do not hide business rules in prose spread across prompts.
2. **Authority is not inferred.** A model may identify a missing permission; it cannot grant it.
3. **Evidence closes the loop.** Completion is a claim that requires named proof.
4. **Ambiguity is observable.** Asking is a valid output, not a failure of autonomy.
5. **Adaptation stays subordinate.** A topology may change how work is done, not what is owed.
6. **Changes are attributable.** Intent versions and approvals must remain auditable.

## Contributing

Open an issue before changing the public contract or its terminology. Small documentation,
test, and implementation improvements may go directly to a pull request. Include tests for
behavior changes and keep live credentials out of fixtures.

## License

[MIT](LICENSE)
