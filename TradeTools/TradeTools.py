import sys
import json
import csv

import app
import app.tools
import app.commands

from datetime import datetime, date, time
from time import sleep

from binance.client import Client
from binance.websockets import BinanceSocketManager

from app import config
from app.tools import Tools
from app.commands import Commands

class Main(object):
    def listen(self):
        self.commands = Commands()
        console = input('Enter command: ')
        action = self.parseInput(console)
        self.commands.execute(action)

    def parseInput(self, input):
        output = input.replace(')', '')
        output = output.split('(');
        command = output[0].lower().replace(' ', '')
        try:
            params = output[1].replace(' ', '');
            if(params.find(',') != -1):
                if(params.find(';') != -1):
                    return 'Using , and ; delimiters together is forbidden! Use , or ; e.g. command(param1, param2) or command(param1; param2)'
                else:
                    return [command, params.split(',')]

            if(params.find(';') != -1):
                if(params.find(',') != -1):
                    return 'Using , and ; delimiters together is forbidden! Use , or ; e.g. command(param1, param2) or command(param1; param2)' 
                else:
                    return [command, params.split(';')]
        except Exception:
            print('No input params')

        return [command]

class Trade(object):
    def __init__(self, products = {}, orderBook = {}, tradeHistory = {}):
        self.products = products
        self.orderBook = orderBook
        self.tradeHistory = tradeHistory

    def genCommandId(self):
        prevfile = ''
        curcommand = ''

        with open('Output_log.csv', 'r') as outputlog:
            reader = csv.DictReader(outputlog)
            for row in reader:
                prevfile = row['Filename']

        with open(prevfile, 'r') as prevoutput:
            reader = csv.DictReader(prevoutput)
            for row in reader:
                prevcommand = int(row['command_id'])
                prevcommand = prevcommand +1
                curcommand = str(prevcommand)

        return curcommand

    def updateOutput(self, time, command_id):
        with open('Output_' + time + '.csv', 'a') as output:
            fieldnames = ['Start_datetime', 'command_id', 'command_full', 'prior_idx', 'cancel_idx', 'start_idx', 'Stop_datetime', 'STATUS']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Start_datetime': time, 'command_id': command_id, 'command_full': 'connect', 'prior_idx': '', 'cancel_idx': '', 'start_idx': '', 'Stop_datetime': '', 'STATUS': 'PROCESS'})

        with open('Output_log.csv', 'a') as outputlog:
            fieldnames = ['Filename', 'datetime']
            writer = csv.DictWriter(outputlog, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Filename': 'Output_' + time + '.csv', 'datetime': time})

    def updateCommand(self, time, command_id):
        with open('Output_' + time + '.csv', 'a') as output:
            fieldnames = ['Start_datetime', 'command_id', 'command_full', 'prior_idx', 'cancel_idx', 'start_idx', 'Stop_datetime', 'STATUS']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Start_datetime': time, 'command_id': command_id, 'command_full': 'connect', 'prior_idx': '', 'cancel_idx': '', 'start_idx': '', 'Stop_datetime': datetime.now().strftime("%Y-%m-%d_%H.%M.%S"), 'STATUS': 'COMPLETED'})

    def connect(self):
        self.tools = Tools(Client(config.api_key, config.api_secret))
        print('Connected to Binance')
        print('Logging...')
        self.curtime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.curcommand = self.genCommandId()
        self.updateOutput(self.curtime, self.curcommand)
        print('Logging done')
        print('Updating data...')
        self.updateData()
        print('Data updated')
        print('Logging...')
        self.updateCommand(self.curtime, self.curcommand)
        print('Logging done')

    def disconnect(self):
        self.tools = None
        print('Logging...')
        self.curcommand = self.genCommandId()
        self.updateOutput(self.curtime, self.curcommand)
        self.updateCommand(self.curtime, self.curcommand)
        print('Logging done')
        print('Disconnected')

    def processMessage(self, msg):
        print("message type: {}".format(msg['e']))
        print(msg)

    def updateData(self):
        self.updateProducts()
        self.updateOrderBook()
        self.updateTradeHistory()

    def updateProducts(self):
        print('Updating products...')
        self.products = self.tools.getProducts()
        with open("./app/output/products.json", "w", encoding="utf-8") as file:
            json.dump(self.products, file)
        print('Products updated')

    def updateOrderBook(self):
        print('Updating order book...')
        for product in self.products:
            self.orderBook[product['symbol']] = self.tools.getOrderBook(product['symbol'])
            sleep(1)

        with open("./app/output/orderbook.json", "w", encoding="utf-8") as file:
            json.dump(self.orderBook, file)

        print('Order book updated')

    def updateTradeHistory(self):
        print('Updating trade history...')
        for product in self.products:
            self.tradeHistory[product['symbol']] = self.tools.getTradeHistory(product['symbol'])
            sleep(1)

        with open("./app/output/tradehistory.json", "w", encoding="utf-8") as file:
            json.dump(self.tradeHistory, file)

        print('Trade history updated')



while True:
    app = Main()
    app.listen()
