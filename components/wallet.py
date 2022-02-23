class wallet():
    def __init__(self, saldo=0, btcAmount=0):
        self.saldo = saldo
        self.btcAmount = btcAmount
        self.trigger = -1
    
    def buyOrder(self, price):
        if self.saldo != 0:
            self.btcAmount = float(self.saldo)/float(price)
            self.saldo = 0

    def sellOrder(self, price):
        if self.btcAmount != 0:
            self.saldo = self.btcAmount*price
            self.btcAmount = 0
    
    def viewWallet(self):
        print('---------------------')
        print(f'BTC = {self.btcAmount}')
        print(f'USD = {self.saldo}')
    
    def smaValue(self, sma1, sma2):
        self.sma1 = sma1
        self.sma2 = sma2
    
    def __del__(self):
        pass
    
    def equity(self, price):
        equity = float(self.saldo) + float(self.btcAmount*price)
        return equity