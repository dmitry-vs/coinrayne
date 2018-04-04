import os
import xml.etree.ElementTree as Etree
import requests

from argparser import parse_args_main_runloop
import binance_exchange
import dates
from signals import find_pumps


# parse args
args = parse_args_main_runloop()
this_script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(this_script_dir, args.input_file)
current_time = dates.currenttime()
output_file = 'trades_{}.txt'.format(current_time.replace(':', '_'))

# read parameters from input file xml
# coins format: {ticker: (timedelta, volume, price, stoploss, takeprofit)}
with open(input_file, 'r') as f:
    input_xml = f.read()
xmltree = Etree.fromstring(input_xml)
xmlcoins = xmltree.findall('coin')
coins = {xmlcoin.attrib['ticker']: (xmlcoin.attrib['timedelta'], float(xmlcoin.attrib['volume']),
                                    float(xmlcoin.attrib['price']), float(xmlcoin.attrib['stoploss']),
                                    float(xmlcoin.attrib['takeprofit']))
         for xmlcoin in xmlcoins}
print(coins)


# create binance client
binance_client = binance_exchange.get_client()
binance_timeframe = binance_exchange.time_frames['1m']

# run loop while printing results to output_file
trades = {}
trade_info_format = '''* {} {}
Buy price: {}
Stop loss price: {}
Take profit price: {}\n'''
open(output_file, 'w+').close()  # create empty output file
while True:
    try:
        print('Total trades: ', trades)
        for key, val in coins.items():
            start_time = 'now - {}  UTC+3'.format(val[0])
            end_time = 'now UTC+3'
            candles = binance_client.get_historical_klines(key, binance_timeframe, start_time, end_time)
            first_candle, last_candle = candles[0], candles[-1]
            first_candle_minute = dates.fromtimestamp(first_candle[0], input_millisec=True)
            last_candle_minute = dates.fromtimestamp(last_candle[0], input_millisec=True)
            current_price = float(last_candle[4])
            pumps = find_pumps(candles, val[1], val[2])

            print('* {} {}'.format(dates.currenttime(), key))
            print('\tFirst candle: ', first_candle_minute)
            print('\tLast candle: ', last_candle_minute)
            print('\tCurrent price: {0:.8f}'.format(current_price))

            if pumps:
                pump_candle_minutes = [dates.fromtimestamp(p, input_millisec=True) for p in pumps]
                print('\tPump candles:', pump_candle_minutes)
                if pumps[-1] == last_candle[0]:  # pump is now
                    if key not in trades:
                        trades[key] = []
                    if pump_candle_minutes[-1] in trades[key]:  # this pump has already been traded
                        continue

                    buy_price = current_price
                    stoploss_price = buy_price * (100 - val[3]) / 100
                    takeprofit_price = buy_price * (100 + val[4]) / 100
                    trades[key].append(pump_candle_minutes[-1])
                    trade_info = trade_info_format.format(dates.currenttime(), key, '{0:.8f}'.format(buy_price),
                                                          '{0:.8f}'.format(stoploss_price), '{0:.8f}'.format(takeprofit_price))

                    print(trade_info)
                    with open(output_file, 'a+') as f:
                        f.write(trade_info)
    except KeyboardInterrupt:
        print('Canceled by user, exit now')
        break
    except requests.exceptions.ReadTimeout:
        continue
