import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path



def create_chart(

        df,

        symbol,

        timeframe="15m"

):


    df = df.copy()



    # если timestamp уже дата

    if "timestamp" in df.columns:


        if not hasattr(

            df["timestamp"].iloc[0],

            "strftime"

        ):

            df["timestamp"] = (

                df["timestamp"]

                .astype("int64")

            )


            df["timestamp"] = (

                df["timestamp"]

                .apply(

                    lambda x:

                    pd.to_datetime(

                        x,

                        unit="ms"

                    )

                )

            )



    df["EMA20"] = (

        df["close"]

        .ewm(span=20)

        .mean()

    )


    df["EMA50"] = (

        df["close"]

        .ewm(span=50)

        .mean()

    )



    folder = Path("charts")

    folder.mkdir(

        exist_ok=True

    )



    path = folder / (

        symbol.replace("/", "_")

        +

        "_"

        +

        timeframe

        +

        ".png"

    )



    fig, ax = plt.subplots(

        figsize=(14,7)

    )



    for _, row in df.iterrows():


        color = (

            "green"

            if row.close >= row.open

            else "red"

        )


        ax.plot(

            [

                row.timestamp,

                row.timestamp

            ],

            [

                row.low,

                row.high

            ],

            color=color

        )


        ax.bar(

            row.timestamp,

            row.close-row.open,

            bottom=row.open,

            width=0.005,

            color=color

        )



    ax.plot(

        df.timestamp,

        df.EMA20,

        label="EMA20"

    )


    ax.plot(

        df.timestamp,

        df.EMA50,

        label="EMA50"

    )



    ax.set_title(

        f"{symbol} {timeframe}"

    )


    ax.legend()



    ax.xaxis.set_major_formatter(

        mdates.DateFormatter(

            "%H:%M"

        )

    )



    plt.tight_layout()



    plt.savefig(

        path,

        dpi=200

    )


    plt.close()



    return str(path)
