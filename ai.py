import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def ai_analyze(data):

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты профессиональный криптоаналитик. Кратко анализируй рынок."
            },
            {
                "role": "user",
                "content": str(data)
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
