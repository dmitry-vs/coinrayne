import argparse
import datetime
import os
import time
import json
from binance.client import Client


def find_pumps(candle_data, percent_limit):
    pump_times = []
    volumes = [float(item[5]) for item in candle_data]
    total_volume = sum(volumes)

    for i in range(0, len(candle_data)):
        if volumes[i] >= total_volume * (percent_limit / 100):
            # check that candle is white - close price higher than open
            open_price = float(candle_data[i][1])
            close_price = float(candle_data[i][4])
            if close_price <= open_price:
                continue
            pump_times.append(candle_data[i][0])

    return pump_times


# parse command line arguments
parser = argparse.ArgumentParser()
required_named_args = parser.add_argument_group('required arguments')
required_named_args.add_argument('-i', dest='time_frame', type=str, required=True,
                                 help='time frame: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w')
required_named_args.add_argument('-p', dest='percent', type=int, required=True,
                                 help='percent of volume change to detect, e.g. 40')
required_named_args.add_argument('-s', dest='start_date', type=str, required=True,
                                 help='start date and time, e.g. "2017-12-28" or "1 day ago"')
# optional
parser.add_argument('-f', dest='tickers_file', type=str, default='coins.txt',
                    help='text file with ticker on each line, default is coins.txt')
parser.add_argument('-e', dest='end_date', type=str, default='now',
                    help='end date and time, e.g. "2017-12-28" or "1 day ago" default is "now"')
args = parser.parse_args()

# make corrections due to UTC+3 timezone
start_date = args.start_date + ' UTC+3'
end_date = args.end_date + ' UTC+3'

# get tickers from file
this_script_dir = os.path.dirname(os.path.realpath(__file__))
tickers_file = os.path.join(this_script_dir, args.tickers_file)
with open(tickers_file) as f:
    tickers = f.readlines()
tickers = [x.strip() for x in tickers]
tickers = [x.replace('/', '') for x in tickers]


# create Binance client
client = Client('', '')
time_frames = {'1m': Client.KLINE_INTERVAL_1MINUTE, '5m': Client.KLINE_INTERVAL_5MINUTE,
               '15m': Client.KLINE_INTERVAL_15MINUTE, '30m': Client.KLINE_INTERVAL_30MINUTE,
               '1h': Client.KLINE_INTERVAL_1HOUR, '2h': Client.KLINE_INTERVAL_2HOUR,
               '4h': Client.KLINE_INTERVAL_4HOUR, '6h': Client.KLINE_INTERVAL_6HOUR,
               '12h': Client.KLINE_INTERVAL_12HOUR, '1d': Client.KLINE_INTERVAL_1DAY,
               '1w': Client.KLINE_INTERVAL_1WEEK}


# process tickers in a loop
total_pumps = {}
for ticker in tickers:
    print(time.strftime("* %Y-%m-%d %H:%M:%S", time.gmtime()), ticker)
    candles = client.get_historical_klines(ticker, time_frames[args.time_frame], start_date, end_date)
    first_candle = candles[0]
    last_candle = candles[-1]
    print('\tFirst candle:', datetime.datetime.fromtimestamp(first_candle[0] / 1e3).strftime("%Y-%m-%d %H:%M"))
    print('\tLast candle:', datetime.datetime.fromtimestamp(last_candle[0] / 1e3).strftime("%Y-%m-%d %H:%M"))
    pumps = find_pumps(candles, args.percent)
    if pumps:
        pumps_readable = [datetime.datetime.fromtimestamp(p / 1e3).strftime("%Y-%m-%d %H:%M") for p in pumps]
        print('\tPump candles:', pumps_readable)
        total_pumps[ticker] = pumps_readable

# print result
print('\nTotal pumps:')
print(json.dumps(total_pumps, indent=1))
