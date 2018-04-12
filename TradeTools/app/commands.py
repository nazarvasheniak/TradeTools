class Commands(object):
    def __init__(self):
        from TradeTools import Trade
        self.trade = Trade()

    def execute(self, action):
        command = action[0]
        if(len(action) > 1):
            params = action[1]
        else:
            params = []
        
        if(command == 'connect'):
            return self.connect(params)
        
        if(command == 'start'):
            return self.start(params)

        if(command == 'list'):
            return self.list(params)

        if(command == 'clean'):
            return self.clean(params)

        if(command == 'stop'):
            return self.stop(params)

        if(command == 'disconnect'):
            return self.disconnect(params)

    def connect(self, params):
        self.trade.connect()

    def start(self, params):
        print('start')
        print(params)

    def list(self, params):
        print('list')
        print(params)

    def clean(self, params):
        print('clean')
        print(params)

    def stop(self, params):
        print('stop')
        print(params)

    def disconnect(self, params):
        print('disconnect')
        print(params)

