from PIL import Image, ImageDraw, ImageFont
import time


def create_chart(candles, symbol="BTC-USDT", signal=None):

    width = 900
    height = 500

    img = Image.new(
        "RGB",
        (width, height),
        "black"
    )

    draw = ImageDraw.Draw(img)


    if not candles:
        draw.text(
            (20,20),
            "NO DATA",
            fill="white"
        )
        return img


    prices = [
        x["close"]
        for x in candles
    ]


    mn = min(prices)
    mx = max(prices)


    def y(price):
        return height - (
            (price-mn)/(mx-mn)
        )*350 - 50


    step = width // len(candles)


    for i,c in enumerate(candles):

        x = i*step+20

        color = (
            "green"
            if c["close"] >= c["open"]
            else "red"
        )


        draw.line(
            (
                x,
                y(c["high"]),
                x,
                y(c["low"])
            ),
            fill=color,
            width=2
        )


        draw.rectangle(
            (
                x-3,
                y(c["open"]),
                x+3,
                y(c["close"])
            ),
            fill=color
        )


    price = candles[-1]["close"]

    draw.line(
        (
            0,
            y(price),
            width,
            y(price)
        ),
        fill="yellow",
        width=2
    )


    draw.text(
        (20,20),
        f"{symbol}  PRICE: {price}",
        fill="white"
    )


    if signal:

        entry = signal.get("entry")
        tp = signal.get("tp")
        sl = signal.get("sl")


        for value,name,color in [
            (entry,"ENTRY","cyan"),
            (tp,"TP","green"),
            (sl,"SL","red")
        ]:

            if value:

                yy=y(value)

                draw.line(
                    (
                        0,
                        yy,
                        width,
                        yy
                    ),
                    fill=color,
                    width=3
                )

                draw.text(
                    (
                        10,
                        yy-20
                    ),
                    f"{name}: {value}",
                    fill=color
                )


    path=f"/tmp/{symbol}_{int(time.time())}.png"

    img.save(path)

    return path
