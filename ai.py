import json

from openai import OpenAI

from config import settings



client = OpenAI(

    api_key=settings.openai_key,

    base_url="https://riskradarai.ru/v1"

)



SYSTEM_PROMPT = """

Ты профессиональный криптоаналитик.

Делай быстрый технический анализ.

Ответ строго:

Монета:
Цена:

Сигнал:
LONG / SHORT / WAIT

Уверенность:

Вход:

Stop Loss:

Take Profit:

Причины:

Риски:


Не выдумывай данные.
Если нет хорошего входа — WAIT.

"""




def analyze_market(
        market,
        technical
):


    payload = {

        "market": market,

        "technical": technical

    }



    response = client.chat.completions.create(


        model=settings.openai_model,


        messages=[


            {

                "role":"system",

                "content":SYSTEM_PROMPT

            },


            {

                "role":"user",

                "content":json.dumps(

                    payload,

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


    return (
        response
        .choices[0]
        .message
        .content
    )
