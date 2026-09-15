from openai import OpenAI
from config import settings


client = OpenAI(
    base_url=settings.openai_base_url,
    api_key=settings.openai_key
)


SYSTEM = """
Ты криптоаналитик.

Тебе приходят готовые данные от Python.
Не рассчитывай индикаторы сам.

Ответ:

🪙 Монета:
💰 Цена:

📊 Сигнал:
LONG / SHORT / WAIT

🎯 Вход:
🛑 Stop Loss:
✅ Take Profit:

Уверенность:

Причины:
- тренд
- RSI
- объём

Риск:
"""


def analyze_market(data):

    try:

        response = client.chat.completions.create(

            model=settings.openai_model,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM
                },

                {
                    "role": "user",
                    "content": str(data)
                }

            ]

        )

        return response.choices[0].message.content


    except Exception as e:

        return f"Ошибка AI: {e}"




def chat_ai(text):

    response = client.chat.completions.create(

        model=settings.openai_model,

        messages=[

            {
                "role":"user",
                "content":text
            }

        ]

    )


    return response.choices[0].message.content
