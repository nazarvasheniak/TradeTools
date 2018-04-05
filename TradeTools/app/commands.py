from enum import Enum

class CommandsList(Enum):
    connect = 1
    start = 2
    list = 3
    clean = 4
    stop = 5
    disconnect = 6

class Commands(object):
    def __init__(self):
        self.commands = CommandsList()

    def connect(self):
        print('connect')

    def start(self):
        print('start')

    def list(self):
        print('list')

    def clean(self):
        print('clean')

    def stop(self):
        print('stop')

    def disconnect(self):
        print('disconnect')
