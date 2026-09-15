import json
from pathlib import Path
from openai import OpenAI
from config import settings

SYSTEM = Path(__file__).resolve().parent.joinpath("master_prompt.txt").read_text(encoding="utf-8")
client = OpenAI(api_key=settings.openai_key)

RUSSIAN = """
Отвечай пользователю на русском языке.
Используй только переданные рыночные данные.
Не выдумывай цены, свечи, объёмы, funding, OI, новости или другие показатели.
Не обещай прибыль и не называй торговый результат гарантированным.
LONG/SHORT являются условными сценариями. Если доказательств недостаточно, выбери WAIT/NO TRADE.
Плечо не должно подаваться как гарантия: объясни, что оно увеличивает и прибыль, и убыток.
Если размер счёта и риск пользователя неизвестны, не придумывай их.
"""

def analyze(payload):
    prompt = (
        "Проанализируй проверенный пакет рыночных данных. "
        "Верни только JSON без markdown.\n\n" +
        json.dumps(payload, ensure_ascii=False, default=str)
    )
    response = client.responses.create(
        model=settings.openai_model,
        instructions=SYSTEM + "\n\n" + RUSSIAN,
        input=prompt,
    )
    text = response.output_text.strip()
    try:
        return json.loads(text)
    except Exception:
        return {"raw": text}

def chat(message, context=None):
    context = context or {}
    response = client.responses.create(
        model=settings.openai_model,
        instructions=SYSTEM + "\n\n" + RUSSIAN,
        input=(
            "Это диалог с пользователем. Текущий контекст анализа:\n" +
            json.dumps(context, ensure_ascii=False, default=str) +
            "\n\nСообщение пользователя:\n" + message
        ),
    )
    return response.output_text.strip()
