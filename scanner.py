from market import get_candles


def calculate_ema(values, period):
    if len(values) < period:
        return sum(values) / len(values)

    return sum(values[-period:]) / period



async def analyze_market(symbol):

    candles = await get_candles(symbol, 100)

    if not candles:
        return {
            "error": "Нет данных рынка"
        }


    closes = [
        c["close"]
        for c in candles
    ]


    last = closes[-1]


    ema20 = calculate_ema(
        closes,
        20
    )

    ema50 = calculate_ema(
        closes,
        50
    )


    # направление

    if last > ema20 > ema50:

        direction = "LONG"

        entry = last

        tp = round(
            entry * 1.015,
            4
        )

        sl = round(
            entry * 0.99,
            4
        )


        text = (
            "🟢 Сигнал LONG\n"
            f"Вход: {entry}\n"
            f"TP: {tp}\n"
            f"SL: {sl}"
        )


    elif last < ema20 < ema50:

        direction = "SHORT"

        entry = last

        tp = round(
            entry * 0.985,
            4
        )

        sl = round(
            entry * 1.01,
            4
        )


        text = (
            "🔴 Сигнал SHORT\n"
            f"Вход: {entry}\n"
            f"TP: {tp}\n"
            f"SL: {sl}"
        )


    else:

        direction = "WAIT"

        entry = last
        tp = None
        sl = None


        text = (
            "⚪ Нет сильного сигнала\n"
            f"Цена: {last}"
        )


    return {

        "symbol": symbol,

        "direction": direction,

        "entry": entry,

        "tp": tp,

        "sl": sl,

        "text": text,

        "candles": candles

    }
