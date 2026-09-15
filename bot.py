import asyncio
import pandas as pd

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import (
    settings,
    validate_settings
)


from market import (
    candles,
    market_snapshot
)


from scanner import scan


from chart import create_chart


from ai import (
    analyze_market,
    chat_ai
)



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



def user_data(uid):

    if uid not in users:

        users[uid] = {

            "symbol":"BTC/USDT",

            "tf":"15m",

            "chat":False,

            "last":{}

        }


    return users[uid]




def menu():

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




def coins_menu():

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
async def start(message: Message):

    user_data(
        message.from_user.id
    )


    await message.answer(

        "NEZZX GRAFIK AI\nВыбери действие",

        reply_markup=menu()

    )





# ==========================
# !график BTC
# ==========================


@dp.message(
    F.text.lower().startswith("!график")
)
async def graphic_command(
        message: Message
):


    args = message.text.split()


    if len(args)<2:

        await message.answer(
            "Пример:\n!график BTC"
        )

        return



    coin = args[1].upper()



    symbol = coin


    if "/" not in symbol:

        symbol += "/USDT"



    if symbol not in SYMBOLS:

        await message.answer(

            "Монеты нет в списке"

        )

        return



    await message.answer(
        "Строю график..."
    )



    try:


        df = await asyncio.to_thread(

            candles,

            symbol,

            "15m"

        )



        file = await asyncio.to_thread(

            create_chart,

            df,

            symbol,

            "15m"

        )



        await message.answer_photo(

            photo=open(
                file,
                "rb"
            ),

            caption=f"{symbol} 15M"

        )


    except Exception as e:


        await message.answer(

            f"Ошибка графика:\n{e}"

        )





@dp.callback_query(
    F.data=="coins"
)
async def coins(
        call: CallbackQuery
):

    await call.message.edit_text(

        "Выбери монету",

        reply_markup=coins_menu()

    )





@dp.callback_query(
    F.data.startswith("coin:")
)
async def select_coin(
        call: CallbackQuery
):

    coin = call.data.split(":")[1]


    user_data(
        call.from_user.id
    )["symbol"] = coin



    await call.message.edit_text(

        f"Выбрано {coin}",

        reply_markup=menu()

    )





@dp.callback_query(
    F.data=="analyze"
)
async def analyze(
        call: CallbackQuery
):

    user = user_data(
        call.from_user.id
    )


    await call.message.answer(
        "Сканирую рынок..."
    )



    data = await asyncio.to_thread(

        market_snapshot,

        user["symbol"],

        user["tf"]

    )



    df = pd.DataFrame(
        data["candles"]
    )



    tech = scan(df)



    result = await asyncio.to_thread(

        analyze_market,

        {

            "market":data,

            "technical":tech

        }

    )



    user["last"] = result



    await call.message.answer(
        result
    )





@dp.callback_query(
    F.data=="chart"
)
async def chart(
        call:CallbackQuery
):

    user=user_data(
        call.from_user.id
    )


    df = await asyncio.to_thread(

        candles,

        user["symbol"],

        user["tf"]

    )


    file = await asyncio.to_thread(

        create_chart,

        df,

        user["symbol"],

        user["tf"]

    )


    await call.message.answer_photo(

        photo=open(
            file,
            "rb"
        )

    )





@dp.callback_query(
    F.data=="chat"
)
async def chat_mode(
        call:CallbackQuery
):

    user_data(
        call.from_user.id
    )["chat"]=True


    await call.message.answer(
        "Chat AI включен"
    )





@dp.message()
async def chat_message(
        message:Message
):

    user=user_data(
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
