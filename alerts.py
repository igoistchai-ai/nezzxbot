alerts = {}



def add_alert(
        user_id,
        symbol,
        price
):

    alerts[str(user_id)] = {

        "symbol": symbol,

        "price": float(price)

    }





def remove_alert(user_id):

    alerts.pop(
        str(user_id),
        None
    )





def get_alerts():

    return alerts





def check_price(prices):


    result = []


    for user, data in list(
        alerts.items()
    ):


        symbol = data["symbol"]


        if symbol in prices:


            current = float(
                prices[symbol]
            )


            target = float(
                data["price"]
            )


            if current >= target:


                result.append({

                    "user": user,

                    "symbol": symbol,

                    "price": current

                })


                del alerts[user]



    return result
