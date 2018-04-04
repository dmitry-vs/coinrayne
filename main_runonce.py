import os
import json

from argparser import parse_args_main_runonce
import binance_exchange
import dates
from signals import find_pumps

# parse command line args
args = parse_args_main_runonce()

# get tickers from file
this_script_dir = os.path.dirname(os.path.realpath(__file__))
tickers_file = os.path.join(this_script_dir, args.tickers_file)
with open(tickers_file) as f:
    tickers = f.readlines()
tickers = [x.strip().replace('/', '') for x in tickers]

# process tickers in a loop
binance_client = binance_exchange.get_client()
total_pumps = {}
for ticker in tickers:
    print('* {} {}'.format(dates.currenttime(), ticker))
    candles = binance_client.get_historical_klines(ticker, binance_exchange.time_frames[args.time_frame],
                                                   args.start_date, args.end_date)
    first_candle, last_candle = candles[0], candles[-1]
    print('\tFirst candle: ', dates.fromtimestamp(first_candle[0], input_millisec=True))
    print('\tLast candle: ', dates.fromtimestamp(last_candle[0], input_millisec=True))
    pumps = find_pumps(candles, args.percent)
    if pumps:
        pumps_readable = [dates.fromtimestamp(p, input_millisec=True) for p in pumps]
        print('\tPump candles:', pumps_readable)
        total_pumps[ticker] = pumps_readable

# print result
print('\nTotal pumps:')
print(json.dumps(total_pumps, indent=1))
