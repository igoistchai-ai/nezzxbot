import os


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-mini"
)


TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)
