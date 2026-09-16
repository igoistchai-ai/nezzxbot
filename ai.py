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

Данные уже рассчитаны.

Отвечай быстро.

Формат:

Монета:
Цена:

Сигнал:
LONG/SHORT/WAIT

Вход:
SL:
TP1:
TP2:

Причина:
3 коротких пункта.

Не гарантируй прибыль.
"""



def analyze_market(data):

    try:

        response = client.chat.completions.create(

            model=OPENAI_MODEL,

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM
                },

                {
                    "role":"user",
                    "content":str(data)
                }

            ]

        )


        return response.choices[0].message.content


    except Exception as e:

        return f"AI ошибка: {e}"





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
