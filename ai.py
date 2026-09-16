from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)



SYSTEM = """
Ты криптоаналитик.

Данные уже рассчитаны системой.

Формат ответа:

🪙 Монета:
💰 Цена:

📊 Сигнал:
LONG / SHORT / WAIT

🎯 Вход:
🛑 SL:
✅ TP:

Причины:
- тренд
- индикаторы
- объём

Не обещай прибыль.
"""



def analyze_market(data):

    response = client.chat.completions.create(

        model=OPENAI_MODEL,

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





def chat_ai(text):

    response = client.chat.completions.create(

        model=OPENAI_MODEL,

        messages=[

            {
                "role":"user",
                "content":text
            }

        ]

    )


    return response.choices[0].message.content
