import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from scanner import analyze_market
from chart import create_chart
from ai import ai_analyze


TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(
    TOKEN
)

dp = Dispatcher()


user_coin = {}


coins = [
    "BTC-USDT",
    "ETH-USDT",
    "LTC-USDT",
    "SOL-USDT"
]


@dp.message(Command("start"))
async def start(message: types.Message):

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="⚡ Быстрый анализ"
                )
            ],
            [
                types.KeyboardButton(
                    text="📊 График"
                )
            ],
            [
                types.KeyboardButton(
                    text="🪙 Монета"
                )
            ],
            [
                types.KeyboardButton(
                    text="💬 Chat"
                )
            ],
        ],
        resize_keyboard=True
    )


    await message.answer(
        "NEZZX AI\nВыберите действие",
        reply_markup=kb
    )



@dp.message(lambda m: m.text=="🪙 Монета")
async def coin_menu(message):

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text=x)
            ]
            for x in coins
        ],
        resize_keyboard=True
    )


    await message.answer(
        "Выберите монету:",
        reply_markup=kb
    )



@dp.message(lambda m: m.text in coins)
async def select_coin(message):

    user_coin[
        message.from_user.id
    ] = message.text


    await message.answer(
        f"Выбрано: {message.text}"
    )



@dp.message(lambda m: m.text=="⚡ Быстрый анализ")
async def fast_analysis(message):

    symbol = user_coin.get(
        message.from_user.id,
        "BTC-USDT"
    )


    msg = await message.answer(
        "⚡ Анализ..."
    )


    try:

        data = await analyze_market(
            symbol
        )


        ai_text = await ai_analyze(
            data
        )


        await msg.edit_text(
            ai_text
        )


    except Exception as e:

        await msg.edit_text(
            f"Ошибка:\n{e}"
        )



@dp.message(lambda m: m.text=="📊 График")
async def graph(message):

    symbol = user_coin.get(
        message.from_user.id,
        "BTC-USDT"
    )


    msg = await message.answer(
        "📈 Рисую график..."
    )


    try:

        data = await analyze_market(
            symbol
        )


        path = create_chart(
            data["candles"],
            symbol,
            data
        )


        photo = FSInputFile(
            path
        )


        await message.answer_photo(
            photo,
            caption=data["text"]
        )


        await msg.delete()


    except Exception as e:

        await msg.edit_text(
            f"Ошибка графика:\n{e}"
        )



async def main():

    await dp.start_polling(
        bot
    )



if __name__=="__main__":

    asyncio.run(
        main()
)
