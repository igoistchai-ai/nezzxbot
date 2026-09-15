import json
from pathlib import Path

from openai import OpenAI

from config import settings



PROMPT_FILE = Path(
    __file__
).parent / "master_prompt.txt"



if PROMPT_FILE.exists():

    SYSTEM_PROMPT = PROMPT_FILE.read_text(
        encoding="utf-8"
    )

else:

    SYSTEM_PROMPT = """
Ты профессиональный криптоаналитик.
Анализируй только переданные данные.
"""



client = OpenAI(

    api_key=settings.openai_key,

    base_url=settings.openai_base_url

)



def analyze_market(data):


    prompt = f"""

Проанализируй рынок:


{json.dumps(
    data,
    ensure_ascii=False,
    indent=2
)}



Ответ:

Монета:

Цена:

Тренд:

Сигнал:
LONG / SHORT / WAIT


Уверенность:

Точка входа:

Stop Loss:

Take Profit:


Причины:

Риски:


Не гарантируй прибыль.
"""



    try:

        response = client.chat.completions.create(

            model=settings.openai_model,


            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )


        return response.choices[0].message.content



    except Exception as e:

        return (
            "Ошибка AI:\n"
            +
            str(e)
        )




def chat_ai(
        message,
        context=None
):

    context = context or {}


    prompt = f"""

Контекст:

{json.dumps(
    context,
    ensure_ascii=False
)}


Вопрос:

{message}

"""



    try:

        response = client.chat.completions.create(

            model=settings.openai_model,


            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )


        return response.choices[0].message.content



    except Exception as e:

        return (
            "Ошибка Chat AI:\n"
            +
            str(e)
        )
