import os
from dataclasses import dataclass


@dataclass
class Settings:

    telegram_token: str = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    openai_key: str = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    openai_model: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-6-astra"
    )

    openai_base_url: str = os.getenv(
        "OPENAI_BASE_URL",
        "https://riskradarai.ru/v1"
    )


    exchange: str = os.getenv(
        "EXCHANGE",
        "okx"
    )


    market_type: str = os.getenv(
        "MARKET_TYPE",
        "spot"
    )


    candle_limit: int = int(
        os.getenv(
            "CANDLE_LIMIT",
            "500"
        )
    )


    cache_seconds: int = int(
        os.getenv(
            "CACHE_SECONDS",
            "15"
        )
    )


settings = Settings()



def validate_settings():

    errors = []


    if not settings.telegram_token:
        errors.append(
            "TELEGRAM_BOT_TOKEN"
        )


    if not settings.openai_key:
        errors.append(
            "OPENAI_API_KEY"
        )


    if errors:

        raise RuntimeError(
            "Нет переменных: "
            +
            ", ".join(errors)
        )
