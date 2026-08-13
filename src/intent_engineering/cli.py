"""Command-line entry point for extraction and deterministic compilation."""

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from openai import OpenAI

from intent_engineering.compiler import IntentCompiler
from intent_engineering.config import Settings
from intent_engineering.extractor import OpenAIIntentExtractor
from intent_engineering.models import IntentSpec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intent-engineering",
        description="Compile an approved intent specification into an execution contract.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--goal", help="Natural-language goal to extract with OpenAI.")
    source.add_argument("--spec", type=Path, help="Path to an approved IntentSpec JSON file.")
    parser.add_argument("--output", type=Path, help="Optional path for the compiled JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.spec:
        spec = IntentSpec.model_validate_json(args.spec.read_text(encoding="utf-8"))
    else:
        settings = Settings()  # type: ignore[call-arg]
        client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
        spec = OpenAIIntentExtractor(client, settings.openai_model).extract(args.goal)

    contract = IntentCompiler().compile(spec)
    output = json.dumps(contract.model_dump(mode="json"), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(f"{output}\n", encoding="utf-8")
    else:
        print(output)
