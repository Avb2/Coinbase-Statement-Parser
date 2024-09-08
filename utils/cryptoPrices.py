import requests


# Gets current crypto prices from Coinbase API public endpoints
def getCryptoPrice(ticker: str):
    btcPriceRequest = requests.get(f"https://api.coinbase.com/v2/prices/{ticker}-USD/buy")
    btcPriceResponse: dict = btcPriceRequest.json()
    price = btcPriceResponse["data"]['amount']

    return float(price)



