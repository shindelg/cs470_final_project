import csv
from prototype import get_data

def check_tickers(fileName):

    successFile = "successful-ticker-test.csv"
    succfile = open(successFile, "w+")

    failFile = "failed-ticker-test.csv"
    failfile = open(failFile, "w+")


#    with open(fileName, newline='') as csvfile:
#        inputReader = csv.reader(csvfile, delimiter=',', quotechar='|')
#        for row in inputReader:
#            tickerList = row

    print("opening file")
    tickerFile = open(fileName, 'r')

    tickers = tickerFile.read()

    tickerList = tickers.split("\n")


    for sym in tickerList:
        holdticker = sym.strip()
        pieces = holdticker.split(':')
        if ':' in sym:
            ticker = pieces[1] + "-" + pieces[0]

            if get_data(ticker) is False:
                print("False")
                failfile.write(sym + ',\n')
            else:
                succfile.write(sym + ',\n')

    succfile.close()
    failfile.close()
    tickerFile.close()


check_tickers("simpleVersion.csv")
