import pytest

from intent_engineering.extractor import _json_object


def test_json_object_accepts_fenced_json() -> None:
    assert _json_object('```json\n{"outcome": "ship"}\n```') == {"outcome": "ship"}


def test_json_object_rejects_arrays() -> None:
    with pytest.raises(ValueError, match="JSON object"):
        _json_object("[]")
