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
    "SOL/USDT",
    "DOGE/USDT"

]


users = {}



def user_data(uid):

    if uid not in users:

        users[uid] = {

            "symbol":"BTC/USDT",

            "chat":False,

            "alert":False

        }


    return users[uid]





def main_menu():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="🚀 Начать анализ",
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
        text="💬 Chat AI",
        callback_data="chat"
    )


    kb.adjust(1)


    return kb.as_markup()




def coins_menu():

    kb=InlineKeyboardBuilder()


    for coin in coins:

        kb.button(

            text=coin,

            callback_data=f"coin_{coin}"

        )


    kb.adjust(2)

    return kb.as_markup()





@dp.message(CommandStart())
async def start(message:Message):


    user_data(
        message.from_user.id
    )


    await message.answer(

        "NEZZX GRAFIK AI\n\nВыберите действие:",

        reply_markup=main_menu()

    )





# =====================
# Анализ
# =====================


@dp.callback_query(
    F.data=="analysis"
)
async def analysis(call:CallbackQuery):


    user=user_data(
        call.from_user.id
    )


    symbol=user["symbol"]


    await call.message.answer(
        "⚡ Сканирую рынок..."
    )



    try:


        df=await asyncio.to_thread(

            get_candles,

            symbol

        )



        technical=scan(df)



        market=get_market_snapshot(

            symbol

        )



        result=await asyncio.to_thread(

            analyze_market,

            market,

            technical

        )



        image=await asyncio.to_thread(

            create_chart,

            df,

            symbol

        )



        await call.message.answer_photo(

            FSInputFile(image),

            caption="📈 График анализа"

        )


        await call.message.answer(

            result

        )



    except Exception as e:


        await call.message.answer(

            f"Ошибка анализа:\n{e}"

        )





# =====================
# Монеты
# =====================


@dp.callback_query(
    F.data=="coins"
)
async def show_coins(call:CallbackQuery):


    await call.message.answer(

        "Выберите монету:",

        reply_markup=coins_menu()

    )





@dp.callback_query(
    F.data.startswith("coin_")
)
async def select_coin(call:CallbackQuery):


    symbol=call.data.replace(
        "coin_",
        ""
    )


    user_data(
        call.from_user.id
    )["symbol"]=symbol



    await call.message.answer(

        f"🪙 Выбрано: {symbol}"

    )





# =====================
# График
# =====================


@dp.callback_query(
    F.data=="chart"
)
async def chart(call:CallbackQuery):


    user=user_data(
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





@dp.message(
    F.text.lower().startswith("!график")
)
async def command_chart(message:Message):


    args=message.text.split()


    if len(args)<2:

        await message.answer(
            "Пример: !график BTC"
        )

        return



    symbol=args[1].upper()



    if "/" not in symbol:

        symbol += "/USDT"



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





# =====================
# Цена
# =====================


@dp.callback_query(
    F.data=="alert"
)
async def price_alert(call:CallbackQuery):


    user_data(
        call.from_user.id
    )["alert"]=True


    await call.message.answer(

        "Введите цену уведомления"

    )





# =====================
# Текст
# =====================


@dp.message()
async def text(message:Message):


    user=user_data(
        message.from_user.id
    )


    if user["alert"]:


        add_alert(

            message.from_user.id,

            user["symbol"],

            float(message.text)

        )


        user["alert"]=False


        await message.answer(

            "🔔 Уведомление установлено"

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
async def enable_chat(call:CallbackQuery):


    user_data(
        call.from_user.id
    )["chat"]=True



    await call.message.answer(

        "💬 Chat AI включён"

    )





async def main():

    validate()

    await dp.start_polling(
        bot
        )
