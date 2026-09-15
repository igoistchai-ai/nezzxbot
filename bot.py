import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings, validate_settings
from market import market_snapshot
from scanner import scan
from ai import analyze, chat

bot = Bot(settings.telegram_token)
dp = Dispatcher()

SYMBOLS = {
    "BTC/USDT": "Bitcoin",
    "ETH/USDT": "Ethereum",
    "LTC/USDT": "Litecoin",
    "SOL/USDT": "Solana",
    "BNB/USDT": "BNB",
    "XRP/USDT": "XRP",
    "DOGE/USDT": "Dogecoin",
    "ADA/USDT": "Cardano",
}
user_state = {}
last_analysis = {}

def main_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="Начать анализ", callback_data="analyze")
    b.button(text="Выбрать монету", callback_data="coins")
    b.button(text="Таймфрейм: 15M", callback_data="tf")
    b.button(text="Chat AI", callback_data="chat")
    b.adjust(1)
    return b.as_markup()

def coins_keyboard():
    b = InlineKeyboardBuilder()
    for symbol, name in SYMBOLS.items():
        b.button(text=name, callback_data=f"coin:{symbol}")
    b.button(text="Назад", callback_data="home")
    b.adjust(2)
    return b.as_markup()

def tf_keyboard():
    b = InlineKeyboardBuilder()
    for tf in ("5m","15m","1h","4h","1d"):
        b.button(text=tf.upper(), callback_data=f"tf:{tf}")
    b.button(text="Назад", callback_data="home")
    b.adjust(3)
    return b.as_markup()

def state(user_id):
    return user_state.setdefault(user_id, {"symbol":"BTC/USDT","timeframe":"15m","chat":False})

@dp.message(CommandStart())
async def start(message: Message):
    state(message.from_user.id)
    await message.answer(
        "NEZZX GRAFIK\n\nВыбери действие:",
        reply_markup=main_keyboard()
    )

@dp.callback_query(F.data == "home")
async def home(c: CallbackQuery):
    state(c.from_user.id)["chat"] = False
    await c.message.edit_text("NEZZX GRAFIK\n\nВыбери действие:", reply_markup=main_keyboard())
    await c.answer()

@dp.callback_query(F.data == "coins")
async def coins(c: CallbackQuery):
    await c.message.edit_text("Выбери монету:", reply_markup=coins_keyboard())
    await c.answer()

@dp.callback_query(F.data.startswith("coin:"))
async def coin(c: CallbackQuery):
    symbol = c.data.split(":",1)[1]
    state(c.from_user.id)["symbol"] = symbol
    await c.message.edit_text(
        f"Выбрано: {symbol}\n\nВыбери действие:",
        reply_markup=main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "tf")
async def tf(c: CallbackQuery):
    await c.message.edit_text("Выбери таймфрейм:", reply_markup=tf_keyboard())
    await c.answer()

@dp.callback_query(F.data.startswith("tf:"))
async def set_tf(c: CallbackQuery):
    state(c.from_user.id)["timeframe"] = c.data.split(":",1)[1]
    await c.message.edit_text(
        f"Таймфрейм: {state(c.from_user.id)['timeframe'].upper()}",
        reply_markup=main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "analyze")
async def do_analyze(c: CallbackQuery):
    uid = c.from_user.id
    s = state(uid)
    await c.answer("Получаю данные...")
    await c.message.edit_text(
        f"Анализирую {s['symbol']} на {s['timeframe'].upper()}.\n"
        "Получаю свежие свечи и рассчитываю технические показатели..."
    )
    try:
        snapshot = await asyncio.to_thread(market_snapshot, s["symbol"], s["timeframe"])
        technical = await asyncio.to_thread(
            lambda: scan(__import__("pandas").DataFrame(snapshot["candles"]))
        )
        payload = {"market": snapshot, "technical_scan": technical}
        result = await asyncio.to_thread(analyze, payload)
        last_analysis[uid] = {"payload": payload, "analysis": result}
        text = format_analysis(s["symbol"], s["timeframe"], result, technical)
        await c.message.edit_text(text, reply_markup=main_keyboard())
    except Exception as e:
        await c.message.edit_text(
            f"Ошибка анализа:\n{str(e)[:1200]}",
            reply_markup=main_keyboard()
        )

def format_analysis(symbol, tf, result, technical):
    if "raw" in result:
        body = result["raw"]
    else:
        direction = result.get("bias") or result.get("direction") or "WAIT"
        conf = result.get("confidence_score", result.get("confidence", "—"))
        entry = result.get("entry_zone", "—")
        stop = result.get("stop_reference", result.get("stop_loss", "—"))
        targets = result.get("targets", {})
        tp1 = targets.get("TP1", targets.get("tp1", "—")) if isinstance(targets, dict) else "—"
        tp2 = targets.get("TP2", targets.get("tp2", "—")) if isinstance(targets, dict) else "—"
        reason = result.get("reason", result.get("reasoning", "—"))
        body = (
            f"{symbol} — {tf.upper()}\n\n"
            f"Направление: {direction}\n"
            f"Уверенность: {conf}/100\n\n"
            f"Вход: {entry}\n"
            f"Стоп / invalidation: {stop}\n"
            f"TP1: {tp1}\n"
            f"TP2: {tp2}\n\n"
            f"Причина:\n{reason}"
        )
    return body + (
        "\n\nТехнический скан:\n"
        f"Trend: {technical['trend']}\n"
        f"RSI: {technical['rsi14']:.1f}\n"
        f"EMA20: {technical['ema20']:.6g}\n"
        f"EMA50: {technical['ema50']:.6g}\n"
        f"Свеча: {technical['candle']}"
    )

@dp.callback_query(F.data == "chat")
async def chat_mode(c: CallbackQuery):
    state(c.from_user.id)["chat"] = True
    await c.message.edit_text(
        "Chat AI включён.\n\nЗадай вопрос сообщением. "
        "Для выхода нажми /start."
    )
    await c.answer()

@dp.message()
async def messages(message: Message):
    uid = message.from_user.id
    s = state(uid)
    if not s.get("chat"):
        await message.answer("Используй кнопки меню.", reply_markup=main_keyboard())
        return
    context = last_analysis.get(uid, {})
    try:
        answer = await asyncio.to_thread(chat, message.text or "", context)
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка Chat AI: {str(e)[:1000]}")

async def main():
    validate_settings()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
