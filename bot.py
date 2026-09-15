import asyncio

import pandas as pd

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import (
    settings,
    validate_settings
)


from market import (
    candles,
    market_snapshot
)


from chart import create_chart


from ai import (
    analyze_market,
    chat_ai
)


from scanner import scan



bot = Bot(
    token=settings.telegram_token
)


dp = Dispatcher()



SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "LTC/USDT",
    "SOL/USDT",
    "DOGE/USDT"
]


users = {}



def get_user(uid):

    if uid not in users:

        users[uid] = {

            "symbol": "BTC/USDT",

            "timeframe": "15m",

            "chat": False,

            "last": {}

        }


    return users[uid]





def main_menu():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="🚀 Начать анализ",
        callback_data="analyze"
    )


    kb.button(
        text="📊 График",
        callback_data="chart"
    )


    kb.button(
        text="🪙 Монета",
        callback_data="coins"
    )


    kb.button(
        text="💬 Chat AI",
        callback_data="chat"
    )


    kb.adjust(1)


    return kb.as_markup()





def coin_menu():

    kb = InlineKeyboardBuilder()


    for coin in SYMBOLS:

        kb.button(

            text=coin,

            callback_data=f"coin:{coin}"

        )


    kb.adjust(2)


    return kb.as_markup()





@dp.message(
    CommandStart()
)
async def start(
        message: Message
):

    get_user(
        message.from_user.id
    )


    await message.answer(

        "NEZZX GRAFIK AI\nВыбери действие:",

        reply_markup=main_menu()

    )





# ==========================
# !график BTC
# ==========================


@dp.message(
    F.text.lower().startswith("!график")
)
async def graphic(
        message: Message
):


    args = message.text.split()


    if len(args) < 2:

        await message.answer(
            "Пример:\n!график BTC"
        )

        return



    coin = args[1].upper()



    if "/" not in coin:

        coin += "/USDT"



    if coin not in SYMBOLS:

        await message.answer(
            "Монета не поддерживается"
        )

        return



    await message.answer(
        "📊 Строю график..."
    )


    try:


        df = await asyncio.to_thread(

            candles,

            coin,

            "15m"

        )



        file = await asyncio.to_thread(

            create_chart,

            df,

            coin,

            "15m"

        )



        await message.answer_photo(

            photo=FSInputFile(file),

            caption=f"{coin} | 15M"

        )


    except Exception as e:


        await message.answer(

            f"Ошибка графика:\n{e}"

        )





@dp.callback_query(
    F.data == "coins"
)
async def coins(
        call: CallbackQuery
):

    await call.message.edit_text(

        "Выбери монету:",

        reply_markup=coin_menu()

    )





@dp.callback_query(
    F.data.startswith("coin:")
)
async def choose_coin(
        call: CallbackQuery
):

    coin = call.data.split(":")[1]


    get_user(
        call.from_user.id
    )["symbol"] = coin



    await call.message.edit_text(

        f"Выбрано: {coin}",

        reply_markup=main_menu()

    )





@dp.callback_query(
    F.data == "analyze"
)
async def analyze(
        call: CallbackQuery
):

    user = get_user(
        call.from_user.id
    )


    await call.message.answer(
        "🔍 Сканирую рынок..."
    )



    try:


        data = await asyncio.to_thread(

            market_snapshot,

            user["symbol"],

            user["timeframe"]

        )



        df = pd.DataFrame(
            data["candles"]
        )



        technical = scan(df)



        result = await asyncio.to_thread(

            analyze_market,

            {

                "market": data,

                "technical": technical

            }

        )



        user["last"] = result



        await call.message.answer(
            result
        )



    except Exception as e:


        await call.message.answer(

            f"Ошибка анализа:\n{e}"

        )





@dp.callback_query(
    F.data == "chart"
)
async def chart(
        call: CallbackQuery
):

    user = get_user(
        call.from_user.id
    )


    await call.message.answer(
        "📈 Создаю график..."
    )



    try:


        df = await asyncio.to_thread(

            candles,

            user["symbol"],

            user["timeframe"]

        )



        file = await asyncio.to_thread(

            create_chart,

            df,

            user["symbol"],

            user["timeframe"]

        )



        await call.message.answer_photo(

            photo=FSInputFile(file)

        )


    except Exception as e:


        await call.message.answer(

            f"Ошибка графика:\n{e}"

        )





@dp.callback_query(
    F.data == "chat"
)
async def chat_enable(
        call: CallbackQuery
):

    get_user(
        call.from_user.id
    )["chat"] = True



    await call.message.answer(

        "💬 Chat AI включен"

    )





@dp.message()
async def chat(
        message: Message
):

    user = get_user(
        message.from_user.id
    )


    if user["chat"]:


        answer = await asyncio.to_thread(

            chat_ai,

            message.text,

            user["last"]

        )


        await message.answer(
            answer
        )





async def main():

    validate_settings()


    await dp.start_polling(
        bot
        )
