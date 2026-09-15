alerts={}


def add_alert(user, symbol, price):
    alerts[user]={
        "symbol":symbol,
        "price":float(price)
    }


def remove_alert(user):
    alerts.pop(user,None)


def check_alerts(prices):
    result=[]

    for user,data in list(alerts.items()):
        symbol=data["symbol"]

        if symbol in prices:
            if float(prices[symbol]) >= data["price"]:
                result.append(
                    {
                        "user":user,
                        "symbol":symbol,
                        "price":prices[symbol]
                    }
                )
                del alerts[user]

    return result
