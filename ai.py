import json
from openai import OpenAI

from config import settings


client = OpenAI(
    api_key=settings.openai_key,
    base_url=settings.openai_base_url
)


SYSTEM_PROMPT = """
Ты профессиональный криптоаналитик.

Анализируй только по переданным данным.

Формат ответа:

🪙 Монета:
💰 Цена:

📊 Сигнал:
LONG / SHORT / WAIT

🎯 Уверенность:
0-100%

📍 Вход:

🛑 Stop Loss:

✅ Take Profit 1:

✅ Take Profit 2:


Причины:
- тренд
- индикаторы
- объём
- свечные модели


Риск:

Не обещай прибыль.
Если сигнала нет — пиши WAIT.
Ответ короткий и точный.
"""


def analyze_market(
        market,
        technical
):

    data = {

        "market": market,

        "technical": technical

    }


    response = client.chat.completions.create(

        model=settings.openai_model,

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": json.dumps(
                    data,
                    ensure_ascii=False
                )
            }

        ]

    )


    return response.choices[0].message.content





def chat_ai(message):

    response = client.chat.completions.create(

        model=settings.openai_model,

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":message
            }

        ]

    )


    return response.choices[0].message.content
