"""OpenAI-backed extraction of a draft intent specification."""

import json
from typing import Any

from openai import OpenAI

from intent_engineering.models import IntentSpec


def _json_object(text: str) -> dict[str, Any]:
    """Accept plain JSON or a single fenced JSON block from a model response."""

    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1])
    value = json.loads(candidate)
    if not isinstance(value, dict):
        raise ValueError("intent extraction must return a JSON object")
    return value


class OpenAIIntentExtractor:
    """Turn ambiguous natural language into a reviewable draft, never final authority."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client = client
        self._model = model

    def extract(self, goal: str) -> IntentSpec:
        schema = json.dumps(IntentSpec.model_json_schema(), ensure_ascii=False)
        response = self._client.responses.create(
            model=self._model,
            input=(
                "Convert the user's goal into JSON matching the supplied schema. "
                "Do not invent permissions. When the goal is ambiguous, use the ask policy. "
                f"Schema: {schema}\nUser goal: {goal}"
            ),
        )
        return IntentSpec.model_validate(_json_object(response.output_text))
