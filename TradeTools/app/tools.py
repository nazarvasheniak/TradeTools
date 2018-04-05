class Tools(object):
    def __init__(self, client):
        self.client = client

    def getProducts(self):
        products = self.client.get_products()
        return products['data']

    def getOrderBook(self, symbol, limit = 1000):
        return self.client.get_order_book(symbol = symbol, limit = limit)

    def getTradeHistory(self, symbol, limit = 500):
        return self.client.get_historical_trades(symbol = symbol, limit = limit)




