# NEZZX GRAFIK — Telegram AI Crypto Analyst

Чистый Telegram-бот без сайта и Mini App.

## Структура

- `run.py` — запуск.
- `bot.py` — Telegram-кнопки и Chat AI.
- `market.py` — публичные OHLCV/ticker данные OKX через CCXT.
- `scanner.py` — базовый технический сканер.
- `ai.py` — подключение OpenAI-модели и master prompt.
- `master_prompt.txt` — большая системная спецификация.
- `config.py` — переменные окружения.

## Запуск

Python 3.11+:

```bash
pip install -r requirements.txt
```

Создай переменные окружения:

```text
TELEGRAM_BOT_TOKEN=...
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-6-astro
```

Затем:

```bash
python run.py
```

## Важно

Бот использует публичные рыночные данные OKX; ключ OKX для чтения публичных свечей не требуется.

Системный prompt хранится локально в `master_prompt.txt` и не попадает в callback-кнопки Telegram.

LONG/SHORT — условные аналитические сценарии, а не гарантия прибыли. Плечо не должно рассматриваться как способ гарантированно увеличить доход.
