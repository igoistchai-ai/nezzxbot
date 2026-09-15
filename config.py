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


    timeframe: str = os.getenv(
        "TIMEFRAME",
        "15m"
    )


    candle_limit: int = int(
        os.getenv(
            "CANDLE_LIMIT",
            "120"
        )
    )


settings = Settings()



def validate():


    errors = []


    if not settings.telegram_token:

        errors.append(
            "TELEGRAM_TOKEN"
        )


    if not settings.openai_key:

        errors.append(
            "OPENAI_API_KEY"
        )


    if errors:

        raise Exception(

            "Нет переменных: "

            +

            ", ".join(errors)

        )
