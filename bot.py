import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import settings, validate

from market import (
    get_candles,
    get_market_snapshot
)

from scanner import scan

from ai import (
    analyze_market,
    chat_ai
)

from chart import create_chart

from alerts import add_alert



bot = Bot(
    token=settings.telegram_token
)


dp = Dispatcher()



coins = [
    "BTC/USDT",
    "ETH/USDT",
    "LTC/USDT",
    "SOL/USDT"
]


users = {}



def get_user(uid):

    if uid not in users:

        users[uid] = {

            "symbol":"BTC/USDT",

            "alert":False,

            "chat":False,

            "direction":"above"

        }


    return users[uid]





def menu():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="⚡ Быстрый анализ",
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
        text="🔔 Цена",
        callback_data="alert"
    )


    kb.button(
        text="💬 Chat",
        callback_data="chat"
    )


    kb.adjust(1)


    return kb.as_markup()





def coin_menu():

    kb=InlineKeyboardBuilder()


    for c in coins:

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

        "NEZZX AI\nВыберите действие",

        reply_markup=menu()

    )





# =====================
# Анализ
# =====================


@dp.callback_query(
    F.data=="analyze"
)
async def analyze(call:CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    symbol=user["symbol"]


    await call.message.answer(
        "⚡ Анализ..."
    )


    try:


        df = await asyncio.to_thread(

            get_candles,

            symbol

        )



        technical = scan(df)



        market = get_market_snapshot(

            symbol

        )



        result = await asyncio.to_thread(

            analyze_market,

            market,

            technical

        )



        image = await asyncio.to_thread(

            create_chart,

            df,

            symbol,

            technical

        )



        await call.message.answer_photo(

            FSInputFile(image),

            caption="📈 Карта сделки"

        )


        await call.message.answer(

            result

        )



    except Exception as e:


        await call.message.answer(

            f"Ошибка:\n{e}"

        )





# =====================
# Монета
# =====================


@dp.callback_query(
    F.data=="coins"
)
async def coins_menu(call:CallbackQuery):


    await call.message.answer(

        "Выберите монету:",

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



    await call.message.answer(

        f"Выбрано: {coin}"

    )





# =====================
# График
# =====================


@dp.callback_query(
    F.data=="chart"
)
async def chart(call:CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    df=await asyncio.to_thread(

        get_candles,

        user["symbol"]

    )


    image=await asyncio.to_thread(

        create_chart,

        df,

        user["symbol"]

    )


    await call.message.answer_photo(

        FSInputFile(image)

    )





# =====================
# Цена
# =====================


@dp.callback_query(
    F.data=="alert"
)
async def alert(call:CallbackQuery):


    get_user(
        call.from_user.id
    )["alert"]=True



    await call.message.answer(

        "Введите цену уведомления\n\n"
        "Пример:\n100000"

    )





# =====================
# Текст
# =====================


@dp.message()
async def text(message:Message):


    user=get_user(
        message.from_user.id
    )


    if user["alert"]:


        add_alert(

            message.from_user.id,

            user["symbol"],

            float(message.text),

            user["direction"]

        )


        user["alert"]=False



        await message.answer(

            "🔔 Уведомление создано"

        )


        return



    if user["chat"]:


        answer=await asyncio.to_thread(

            chat_ai,

            message.text

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





@dp.message(
    F.text.lower().startswith("!график")
)
async def graphic(message:Message):


    args=message.text.split()


    if len(args)<2:

        await message.answer(
            "Пример: !график BTC"
        )

        return



    symbol=args[1].upper()


    if "/" not in symbol:

        symbol+="/USDT"



    df=await asyncio.to_thread(

        get_candles,

        symbol

    )


    image=await asyncio.to_thread(

        create_chart,

        df,

        symbol

    )


    await message.answer_photo(

        FSInputFile(image)

    )





async def main():

    validate()


    await dp.start_polling(
        bot
)
