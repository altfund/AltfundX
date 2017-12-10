from coinmarketcap import Market
import csv, datetime
import sys
import os

savedir = os.getcwd() #input("Enter the path of your save directory: ")

assert os.path.exists(savedir), "I did not find the file at, "+str(savedir)

coinmarketcap = Market()
coinmarket_ticker_data = coinmarketcap.ticker(convert = 'USD')

with open(os.path.join(savedir, 'coinmarketcap_ticker_data_dump.csv'),'w', newline = '') as myfile:
    wr = csv.writer(myfile) #, quoting=csv.QUOTE_ALL)
    wr.writerow([' ID ', 'NAME', 'SYMBOL', 'RANK', 'PRICE_USD', 'PRICE_BTC', '24H_VOLUMNE_USD', 'MARKET_CAP_USD', 'AVAILABLE SUPPLY',
                 'TOTAL_SUPPLY', 'MAX_SUPPLY', '%1HR', '%24HR', '%7D', "LAST UPDATED", "TIMESTAMP"])
    for i in range(len(coinmarket_ticker_data)):
        wr.writerow(
            [coinmarket_ticker_data[i]['id'],
            coinmarket_ticker_data[i]['name'],
            coinmarket_ticker_data[i]['symbol'],
            coinmarket_ticker_data[i]['rank'],
            coinmarket_ticker_data[i]['price_usd'],
            coinmarket_ticker_data[i]['price_btc'],
            coinmarket_ticker_data[i]['24h_volume_usd'],
            coinmarket_ticker_data[i]['market_cap_usd'],
            coinmarket_ticker_data[i]['available_supply'],
            coinmarket_ticker_data[i]['total_supply'],
            coinmarket_ticker_data[i]['max_supply'],
            coinmarket_ticker_data[i]['percent_change_1h'],
            coinmarket_ticker_data[i]['percent_change_24h'],
            coinmarket_ticker_data[i]['percent_change_7d'],
            coinmarket_ticker_data[i]['last_updated'],
            datetime.datetime.now()]
        )
print("Done, check the provided output directory.")
