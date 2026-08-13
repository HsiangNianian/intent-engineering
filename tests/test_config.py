from intent_engineering.config import Settings, create_openai_client


def test_settings_loads_dotenv(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        (
            "OPENAI_API_KEY=test-key\n"
            "OPENAI_MODEL=test-model\n"
            "OPENAI_BASEURL=https://gateway.example/v1\n"
        ),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key.get_secret_value() == "test-key"
    assert settings.openai_model == "test-model"
    assert settings.openai_baseurl == "https://gateway.example/v1"

    client = create_openai_client(settings)
    try:
        assert str(client.base_url) == "https://gateway.example/v1/"
    finally:
        client.close()


def test_blank_base_url_uses_sdk_default(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=test-key\nOPENAI_BASEURL=  \n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_baseurl is None
