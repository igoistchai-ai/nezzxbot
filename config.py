import os
from dataclasses import dataclass


@dataclass
class Settings:

    # Telegram

    telegram_token: str = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )


    # AI API (RiskRadar)

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



    # Биржа

    exchange: str = os.getenv(
        "EXCHANGE",
        "okx"
    )


    market_type: str = os.getenv(
        "MARKET_TYPE",
        "spot"
    )



    # Анализ

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



    # Render

    port: int = int(
        os.getenv(
            "PORT",
            "4000"
        )
    )



settings = Settings()



def validate():

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

        raise Exception(

            "Отсутствуют переменные: "
            +
            ", ".join(errors)

        )
