from app import config
from app.tools import Tools

from binance.client import Client

#class Trade(object):
#    def __init__(self, products = {}, orderBook = {}, tradeHistory = {}):
#        self.tools = Tools(Client(config.api_key, config.api_secret))
#        self.products = products
#        self.orderBook = orderBook
#        self.tradeHistory = tradeHistory

#    def updateData(self):
#        self.updateProducts()
#        self.updateOrderBook()
#        self.updateTradeHistory()

#    def updateProducts(self):
#        self.products = self.tools.getProducts()

#    def updateOrderBook(self):
#        for product in self.products:
#            self.orderBook[product['symbol']] = self.tools.getOrderBook(product['symbol'])

#    def updateTradeHistory(self):
#        for product in self.products:
#            self.tradeHistory[product['symbol']] = self.tools.getTradeHistory(product['symbol'])


class Main(object):
    def listen(self):
        console = input('Enter command: ')
        action = self.parseInput(console)
        print(action)

    def parseInput(self, input):
        output = input.replace(')', '')
        output = output.split('(');
        command = output[0].lower().replace(' ', '')
        params = output[1].replace(' ', '');

        if(params.find(',') != -1):
            if(params.find(';') != -1):
                return 'Using , and ; delimiters together is forbidden! Use , or ; e.g. command(param1, param2) or command(param1; param2)'
            else:
                return [command, params.split(',')]
        elif(params.find(';') != -1):
            if(params.find(',') != -1):
                return 'Using , and ; delimiters together is forbidden! Use , or ; e.g. command(param1, param2) or command(param1; param2)'
            else:
                return [command, params.split(';')]

app = Main()
app.listen()
