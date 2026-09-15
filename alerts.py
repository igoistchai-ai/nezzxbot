alerts = {}



def add_alert(
        user_id,
        symbol,
        target_price
):

    alerts[user_id] = {

        "symbol": symbol,

        "price": float(target_price)

    }





def remove_alert(
        user_id
):

    if user_id in alerts:

        del alerts[user_id]





def get_alerts():

    return alerts





def check_price(
        prices
):

    triggered = []


    for user, alert in list(
        alerts.items()
    ):

        symbol = alert["symbol"]


        if symbol in prices:


            current = float(
                prices[symbol]
            )


            target = float(
                alert["price"]
            )


            if current >= target:


                triggered.append({

                    "user": user,

                    "symbol": symbol,

                    "price": current

                })


                del alerts[user]



    return triggered
