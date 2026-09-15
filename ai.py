import json

from openai import OpenAI

from config import settings



client = OpenAI(

    api_key=settings.openai_key,

    base_url=settings.openai_base_url

)



SYSTEM = """

Ты быстрый криптоаналитик.

Делай технический анализ.

Не пиши длинно.

Формат:

Монета:
Цена:

Сигнал:
LONG/SHORT/WAIT

Уверенность:

Вход:

Stop Loss:

Take Profit:

Причина:

Риск:

"""



def analyze_market(data):


    try:


        response = client.chat.completions.create(

            model=settings.openai_model,


            messages=[

                {
                "role":"system",
                "content":SYSTEM
                },


                {
                "role":"user",
                "content":json.dumps(
                    data,
                    ensure_ascii=False
                )
                }

            ]

        )


        return (
            response
            .choices[0]
            .message
            .content
        )



    except Exception as e:

        return f"AI ошибка: {e}"




def chat_ai(message, context=None):


    response = client.chat.completions.create(

        model=settings.openai_model,


        messages=[

            {
            "role":"system",
            "content":SYSTEM
            },

            {
            "role":"user",
            "content":message
            }

        ]

    )


    return (
        response
        .choices[0]
        .message
        .content
    )
