alerts = {}



def add_alert(
        user_id,
        symbol,
        price,
        direction="above"
):

    alerts[str(user_id)] = {

        "symbol": symbol,

        "price": float(price),

        "direction": direction

    }





def remove_alert(
        user_id
):

    alerts.pop(
        str(user_id),
        None
    )





def get_alerts():

    return alerts





def check_price(prices):


    triggered = []



    for user_id, alert in list(
        alerts.items()
    ):



        symbol = alert["symbol"]



        if symbol not in prices:

            continue



        current = float(

            prices[symbol]

        )


        target = float(

            alert["price"]

        )



        direction = alert.get(

            "direction",

            "above"

        )



        hit = False



        if direction == "above":


            if current >= target:

                hit = True



        elif direction == "below":


            if current <= target:

                hit = True





        if hit:


            triggered.append({

                "user": user_id,

                "symbol": symbol,

                "price": current

            })


            del alerts[user_id]



    return triggered
