
from utils.textCell import TextFormat


# Returns percent return by asset based on avg price
def percentReturn(statement , asset: str, **kwargs) -> float:
    avgPrice = statement.avgPrice(asset=asset)

    percent = kwargs.get("percent")

    if percent:
        return avgPrice + (avgPrice * (percent / 100))
    else:
        returnString = [
            '\n'
            f'{TextFormat.cell(asset)}',
            f'{TextFormat.border()}',
            f'{TextFormat.cell("Percent Change")}{TextFormat.cell("Target Price")}',
            f'{TextFormat.border()}{TextFormat.border()}',
            f'{TextFormat.cell("+5%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (5 / 100))))}',
            f'{TextFormat.cell("+10%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (10 / 100))))}',
            f'{TextFormat.cell("+15%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (15 / 100))))}',
            f'{TextFormat.cell("+20%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (20 / 100))))}',
            f'{TextFormat.cell("+25%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (25 / 100))))}',
            f'{TextFormat.cell("+30%")}{TextFormat.cell("{:.2f}".format(avgPrice + (avgPrice * (30 / 100))))}'
         ]
        
        return returnString
