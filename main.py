from statements.readCoinbaseStatement import CoinbaseStatement

if __name__ == "__main__":
    # Creates a coinbase statement object
    statement = CoinbaseStatement("/Users/exampleUser/Desktop/coinbaseStatement.numbers")
    # Parses the file and stores file information in statement.statements
    statement.readStatement()
    # Generates a report of the statement, using kwarg 'write' to write the statement information to default filepath './monthlyAnalysis.txt'
    # Or define a custom file path using kwarg 'writepath'
    # statement.analyze(write="w", writepath="./myCustomFilePath.txt")
    statement.analyze(write="w")
    
    