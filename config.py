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
        "gpt-5.6-luna"
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


settings = Settings()



def validate_settings():

    missing = []

    if not settings.telegram_token:
        missing.append(
            "TELEGRAM_BOT_TOKEN"
        )

    if not settings.openai_key:
        missing.append(
            "OPENAI_API_KEY"
        )


    if missing:
        raise RuntimeError(
            "Отсутствуют: "
            +
            ", ".join(missing)
        )
