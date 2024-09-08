from numbers_parser import Document



class UsaaStatement:
    def __init__(self, statementPath: str) -> None:
        self.statementPath = statementPath
        self.statement = None

    # Parses statement and assigns it to self.statements
    def readStatement(self):
        document = Document(self.statementPath)
        sheet1 = document.sheets[0]
        rows = sheet1.tables[0].rows()
        self.statement = rows
    
    # Calculates amount spent on a specific asset
    def amountSpentByAsset(self, asset):
        total = 0
        for row in self.statement:
            name = row[1].value
            if name == asset:
                total -= int(row[4].value)  
        return total
        

