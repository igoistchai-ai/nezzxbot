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

from scanner import scan

from ai import (
    analyze_market,
    chat_ai
)

from alerts import add_alert


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

            "symbol":"BTC/USDT",

            "timeframe":"15m",

            "chat":False,

            "alert":False,

            "last":{}

        }

    return users[uid]





def menu():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="🚀 Быстрый анализ",
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
        text="🔔 Уведомление цены",
        callback_data="alert"
    )


    kb.button(
        text="💬 Chat AI",
        callback_data="chat"
    )


    kb.adjust(1)


    return kb.as_markup()





def coin_menu():

    kb = InlineKeyboardBuilder()


    for c in SYMBOLS:

        kb.button(
            text=c,
            callback_data=f"coin:{c}"
        )


    kb.adjust(2)


    return kb.as_markup()





@dp.message(CommandStart())
async def start(message:Message):

    get_user(
        message.from_user.id
    )


    await message.answer(

        "NEZZX GRAFIK AI\n\nВыбери действие:",

        reply_markup=menu()

    )





# =====================
# ГРАФИК
# =====================


@dp.message(
    F.text.lower().startswith("!график")
)
async def graphic(message:Message):


    args = message.text.split()


    if len(args)<2:

        await message.answer(
            "Пример:\n!график BTC"
        )

        return



    symbol=args[1].upper()


    if "/" not in symbol:

        symbol += "/USDT"



    await message.answer(
        "📊 Создаю график..."
    )


    try:

        df = await asyncio.to_thread(

            candles,

            symbol,

            "15m",

            100

        )


        file = await asyncio.to_thread(

            create_chart,

            df,

            symbol,

            "15m"

        )


        await message.answer_photo(

            photo=FSInputFile(file)

        )


    except Exception as e:


        await message.answer(
            f"Ошибка:\n{e}"
        )





# =====================
# ВЫБОР МОНЕТЫ
# =====================


@dp.callback_query(
    F.data=="coins"
)
async def coins(call:CallbackQuery):


    await call.message.edit_text(

        "Выбери монету:",

        reply_markup=coin_menu()

    )





@dp.callback_query(
    F.data.startswith("coin:")
)
async def choose_coin(call:CallbackQuery):


    coin=call.data.split(":")[1]


    get_user(
        call.from_user.id
    )["symbol"]=coin



    await call.message.edit_text(

        f"Выбрано: {coin}",

        reply_markup=menu()

    )





# =====================
# БЫСТРЫЙ АНАЛИЗ
# =====================


@dp.callback_query(
    F.data=="analyze"
)
async def analyze(call:CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    await call.message.answer(
        "⚡ Быстрый анализ..."
    )


    try:


        data = await asyncio.to_thread(

            market_snapshot,

            user["symbol"],

            user["timeframe"]

        )


        df = await asyncio.to_thread(

            candles,

            user["symbol"],

            user["timeframe"],

            100

        )


        technical = scan(df)



        result = await asyncio.to_thread(

            analyze_market,

            {

                "market":data,

                "technical":technical

            }

        )



        user["last"]=result



        await call.message.answer(
            result
        )


    except Exception as e:


        await call.message.answer(
            f"Ошибка анализа:\n{e}"
        )





# =====================
# ГРАФИК КНОПКА
# =====================


@dp.callback_query(
    F.data=="chart"
)
async def chart(call:CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    await call.message.answer(
        "📈 Рисую..."
    )


    df=await asyncio.to_thread(

        candles,

        user["symbol"],

        "15m",

        100

    )


    file=await asyncio.to_thread(

        create_chart,

        df,

        user["symbol"],

        "15m"

    )


    await call.message.answer_photo(

        photo=FSInputFile(file)

    )





# =====================
# ALERT
# =====================


@dp.callback_query(
    F.data=="alert"
)
async def alert(call:CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    user["alert"]=True


    await call.message.answer(

        "🔔 Введи цену.\n\nПример:\n100000"

    )





@dp.message()
async def text(message:Message):


    user=get_user(
        message.from_user.id
    )


    # ввод цены

    if user.get("alert"):


        try:

            price=float(
                message.text
            )


            add_alert(

                message.from_user.id,

                user["symbol"],

                price

            )


            user["alert"]=False


            await message.answer(

                f"🔔 Уведомление создано\n"
                f"{user['symbol']} → {price}"

            )


            return


        except:

            pass




    # CHAT AI


    if user["chat"]:


        answer=await asyncio.to_thread(

            chat_ai,

            message.text,

            user["last"]

        )


        await message.answer(
            answer
        )





@dp.callback_query(
    F.data=="chat"
)
async def chat(call:CallbackQuery):


    get_user(
        call.from_user.id
    )["chat"]=True


    await call.message.answer(

        "💬 Chat AI включён"

    )





async def main():

    validate_settings()


    await dp.start_polling(
        bot
    )
