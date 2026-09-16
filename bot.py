import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


from config import (
    TELEGRAM_TOKEN,
    validate
)

from market import get_candles

from scanner import scan

from chart import create_chart

from ai import analyze_market, chat_ai

from alerts import add_alert



bot = Bot(
    token=TELEGRAM_TOKEN
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

            "symbol": "BTC/USDT",

            "chat": False,

            "alert": False

        }


    return users[uid]





def menu():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="⚡ Анализ",
        callback_data="analysis"
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





@dp.message(CommandStart())
async def start(message: Message):

    get_user(
        message.from_user.id
    )


    await message.answer(
        "NEZZX AI V2\nВыбери действие:",
        reply_markup=menu()
    )





# =========================
# БЫСТРЫЙ АНАЛИЗ
# =========================


@dp.callback_query(
    F.data=="analysis"
)
async def analysis(call: CallbackQuery):


    user = get_user(
        call.from_user.id
    )


    symbol = user["symbol"]



    await call.message.answer(
        "⚡ Быстрый скан..."
    )


    try:


        # получаем свечи

        df = await asyncio.to_thread(

            get_candles,

            symbol

        )


        # python анализ

        technical = scan(

            df,

            symbol

        )


        # график сразу

        image = await asyncio.to_thread(

            create_chart,

            df,

            symbol,

            technical

        )


        await call.message.answer_photo(

            FSInputFile(image),

            caption=(

                f"📈 {symbol}\n"

                f"Цена: {technical['price']}\n"

                f"Сигнал: {technical['signal']}"

            )

        )



        # AI отдельно

        answer = await asyncio.to_thread(

            analyze_market,

            technical

        )


        await call.message.answer(
            answer
        )



    except Exception as e:


        await call.message.answer(

            f"Ошибка:\n{e}"

        )





# =========================
# ГРАФИК
# =========================


@dp.callback_query(
    F.data=="chart"
)
async def chart(call: CallbackQuery):


    user=get_user(
        call.from_user.id
    )


    df = await asyncio.to_thread(

        get_candles,

        user["symbol"]

    )


    technical = scan(
        df,
        user["symbol"]
    )


    image = await asyncio.to_thread(

        create_chart,

        df,

        user["symbol"],

        technical

    )


    await call.message.answer_photo(

        FSInputFile(image)

    )





# =========================
# CHAT
# =========================


@dp.callback_query(
    F.data=="chat"
)
async def chat(call: CallbackQuery):


    get_user(
        call.from_user.id
    )["chat"]=True


    await call.message.answer(
        "💬 Chat AI включён"
    )





@dp.message()
async def text(message: Message):


    user=get_user(
        message.from_user.id
    )


    if user["chat"]:


        answer = await asyncio.to_thread(

            chat_ai,

            message.text

        )


        await message.answer(
            answer
        )





async def main():

    validate()

    await dp.start_polling(
        bot
)
