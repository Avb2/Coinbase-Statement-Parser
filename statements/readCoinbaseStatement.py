from numbers_parser import Document
from model.banking.coinbaseStatementRow import CBStatementRow
from utils.percentReturn import percentReturn
from utils.textCell import TextFormat
from utils.cryptoPrices import getCryptoPrice


class CoinbaseStatement:
    def __init__(self, statementPath) -> None:
        self.csvpath = statementPath
        self.statements = None
    
    # Run this to populate self.statements
    def readStatement(self) -> None:
        document = Document(self.csvpath)
        sheet1 = document.sheets[0]
        rows = sheet1.tables[0].rows()

        statements = [CBStatementRow([x.value for x in row]) for row in rows]
        self.statements = statements

    # Returns all tickers from monthly statement
    def tickerActivity(self) -> list:
        statementTickers = set(x.ticker for x in self.statements)
      
        for x in [None, "Asset"]:
            statementTickers.remove(x)
        return list(statementTickers)

    # Returns the amount in USD bought
    def amtBoughtUSD(self, **kwargs) -> float:
        asset = kwargs.get("asset", None)

        statementTickers = self.tickerActivity()
        total = 0
        amounts = {}
        for x in statementTickers:
            amounts.__setitem__(x, 0)
        
        for row in self.statements:
            if asset and row.ticker == asset and row.type == "Buy":
                amounts.update({row.ticker: amounts.get(row.ticker) + row.amountSpent})
                total += row.amountSpent
            elif not asset and row.type == "Buy":
                amounts.update({row.ticker: amounts.get(row.ticker) + row.amountSpent})
                total += row.amountSpent
        return float("{:.2f}".format(total))
    
    # Returns the amount in USD sold
    def amtSoldUSD(self, **kwargs) -> float:
        asset = kwargs.get("asset", None)

        price = 0
        for x in self.statements:
            if asset and x.ticker == asset and x.type == "Sell":
                price += x.amountSpent
            elif not asset and x.type == "Sell":
                price += x.amountSpent
        return float("{:.2f}".format(price))

    # Returns amount bought - amount sold
    def netAmt(self, **kwargs) -> float:
        asset = kwargs.get("asset", None)

        if asset:
            return float("{:.2f}".format(self.amtBoughtUSD(asset=asset) - self.amtSoldUSD(asset=asset)))
        else:
            return float("{:.2f}".format(self.amtBoughtUSD() - self.amtSoldUSD()))

    # Shows all price points assets were purchased at
    def priceSpreadByAsset(self, asset: str) -> list:
        spread = list()
        for x in self.statements:
            if asset and x.ticker == asset:
                spread.append(x.boughtPrice)

        spread.sort()
        return spread

    # Returns the average purchase price per asset
    def avgPrice(self, **kwargs):
       
        asset = kwargs.get('asset', None)
        
        if asset:
            totalCoin = list()
            totalBuyIn = list()
            for x in self.statements:
                if x.ticker == asset:
                    totalCoin.append(x.coinAmt)
                    totalBuyIn.append(x.coinAmt * x.boughtPrice)
            return float("{:.2f}".format(sum(totalBuyIn) / sum(totalCoin)))
        else:
            data = {}

            for x in self.statements:
                if x.ticker == None or x.ticker == "Asset":
                    pass
                else:
                    currentTotals: dict  = data.get(x.ticker, {"totalCoin": 0, "totalBuyIn": 0})

                    currentCoinAmt = currentTotals.get("totalCoin")
                    currentBoughtPrice = currentTotals.get("totalBuyIn")

                    data.update({x.ticker: {"totalCoin": float(currentCoinAmt + x.coinAmt), "totalBuyIn": float(currentBoughtPrice + (x.coinAmt * x.boughtPrice))}})
            
            keys = data.keys()
            returnData = {}
            for x in keys:
                returnData.update({x: {"avgPrice": float("{:.2f}".format(data.get(x)["totalBuyIn"] / data.get(x)["totalCoin"]))}})
            return returnData
    
    # Runs a full analysis on the statement
    def analyze(self, **kwargs):
        write = kwargs.get("write")

        tickers: list = self.tickerActivity()
        tickers.sort()
        
        amtBought = "{:,.2f}".format(self.amtBoughtUSD())
        amtSold = "{:,.2f}".format(self.amtSoldUSD())
        netAmt = "{:,.2f}".format(self.netAmt())

        

        totalBought = f"{TextFormat.cell('Total Amount Purchased')}{TextFormat.cell(amtBought)}"
        totalSold = f"{TextFormat.cell('Total Amount Sold')}{TextFormat.cell(amtSold)}"
        totalNetAmt = f"{TextFormat.cell('Net Amount Bought/Sold')}{TextFormat.cell(netAmt)}"

        tickerStrings = [f"{TextFormat.cell(ticker)}{TextFormat.cell(self.avgPrice(asset=ticker))}{TextFormat.cell('{:.2f}'.format(min(self.priceSpreadByAsset(asset=ticker))))}{TextFormat.cell('{:.2f}'.format(max(self.priceSpreadByAsset(asset=ticker))))}{TextFormat.cell('{:.2f}'.format(getCryptoPrice(ticker=ticker)))}{TextFormat.cell('{:.2f}'.format(percentReturn(statement=self, percent=20, asset=ticker)))}" for ticker in tickers]
        
        
       
       
        if write:
            summaryContent = [
                "".join([TextFormat.cell("Tickers"), TextFormat.cell("Avg. Purchase Price"), TextFormat.cell("Min Purchase Price"), TextFormat.cell("Max Purchase Price"), TextFormat.cell("Current Price"), TextFormat.cell("+20% Target Return ")]),
                "\n",
                TextFormat.border(),
                TextFormat.border(),
                TextFormat.border(),
                TextFormat.border(),
                TextFormat.border(),
                TextFormat.border(),
                
                "\n",
                "\n".join(tickerStrings),
                "\n",
                TextFormat.border(),TextFormat.border(),TextFormat.border(),TextFormat.border(),TextFormat.border(),TextFormat.border(),
                "\n",
            
                totalBought,
                "\n",
                totalSold,
                "\n",
                TextFormat.border(),TextFormat.border(),
                "\n",
                totalNetAmt,"\n",
                
                TextFormat.border(),TextFormat.border(),
                "\n",
            ]
           
            writepath = kwargs.get("writepath", "./monthlyAnalysis.txt")
            with open(writepath, "w") as file:
                file.writelines(summaryContent)

        else:
             summaryContent = [
                "|   Tickers              |   Avg. Purchase Price                  |",
                "|--------------------------------------------------------|",
                "\n".join(tickerStrings),
                "|--------------------------------------------------------|",
            
                totalBought,
                totalSold,
                "|--------------------------------------------------------|",
                totalNetAmt,
                
                "|--------------------------------------------------------|"
            ]
             
             
             for x in summaryContent:
                 print(x)


