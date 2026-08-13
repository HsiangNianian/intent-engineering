from intent_engineering.config import Settings


def test_settings_loads_dotenv(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=test-key\nOPENAI_MODEL=test-model\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key.get_secret_value() == "test-key"
    assert settings.openai_model == "test-model"
