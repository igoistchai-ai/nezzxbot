import json
from pathlib import Path

from openai import OpenAI

from config import settings



prompt_file = Path(
    __file__
).parent / "master_prompt.txt"



if prompt_file.exists():

    SYSTEM_PROMPT = prompt_file.read_text(
        encoding="utf-8"
    )

else:

    SYSTEM_PROMPT = """
Ты AI криптоаналитик.
Анализируй только переданные данные.
"""


client = OpenAI(

    api_key=settings.openai_key,

    base_url=settings.openai_base_url

)



def analyze_market(data):


    request = f"""

Проанализируй график:

{json.dumps(
    data,
    ensure_ascii=False,
    indent=2
)}



Дай ответ:

Монета:
Цена:

Тренд:

Решение:
LONG / SHORT / WAIT


Уверенность:

Вход:

Stop Loss:

TP1:

TP2:

TP3:


Объяснение:

Риски:


Не обещай прибыль.
Если сигнала нет — WAIT.

"""


    try:


        result = client.chat.completions.create(

            model=settings.openai_model,


            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },


                {
                    "role":"user",
                    "content":request
                }

            ],


            temperature=0.2

        )


        return result.choices[0].message.content



    except Exception as e:


        return (
            "Ошибка AI:\n"
            +
            str(e)
        )




def chat_ai(message, context=None):


    context = context or {}


    request = f"""

Контекст:

{json.dumps(
    context,
    ensure_ascii=False
)}


Вопрос:

{message}

"""


    try:

        result = client.chat.completions.create(

            model=settings.openai_model,


            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":request
                }

            ]

        )


        return result.choices[0].message.content



    except Exception as e:


        return (
            "Ошибка Chat AI:\n"
            +
            str(e)
        )
