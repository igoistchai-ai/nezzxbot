import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def ai_analyze(
    market_data
):

    try:

        prompt = f"""
Ты быстрый крипто-аналитик.

Монета: {market_data.get('symbol')}

Направление:
{market_data.get('direction')}

Цена:
{market_data.get('entry')}

TP:
{market_data.get('tp')}

SL:
{market_data.get('sl')}

Свечи:
последние данные получены.

Ответь коротко:

1. Ситуация рынка
2. Входить или ждать
3. Риск

Не пиши длинный текст.
"""


        response = client.chat.completions.create(

            model="gpt-5-mini",

            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            max_tokens=150

        )


        return response.choices[0].message.content


    except Exception as e:

        return (
            "AI ошибка: "
            + str(e)
        )
