
class CBStatementRow:
    def __init__(self, data):
        self.id = data[0]
        self.date = data[1]
        self.type = data[2]
        self.ticker = data[3]
        self.coinAmt = data[4]
        self.boughtWith = data[5]
        self.boughtPrice = data[6]
        self.amountSpent = data[7]
        self.summary = data[-1]


    def __dict__(self):
        return {
            'id': self.id,
            'date': self.date,
            'type': self.type, 
            "ticker": self.ticker, 
            "coinAmt": self.coinAmt, 
            "boughtWith": self.boughtWith,
            "boughtPrice": self.boughtPrice, 
            "amountSpent": self.amountSpent,
            "summary": self.summary
        }

