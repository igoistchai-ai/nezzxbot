import os



# Telegram

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""
)



# OpenAI

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-mini"
)



# Market

TIMEFRAME = os.getenv(
    "TIMEFRAME",
    "15m"
)


CANDLE_LIMIT = int(
    os.getenv(
        "CANDLE_LIMIT",
        "120"
    )
)





def validate():

    errors = []


    if not TELEGRAM_TOKEN:

        errors.append(
            "TELEGRAM_BOT_TOKEN"
        )


    if not OPENAI_API_KEY:

        errors.append(
            "OPENAI_API_KEY"
        )



    if errors:

        raise Exception(

            "Отсутствуют Environment переменные: "

            +

            ", ".join(errors)

        )
