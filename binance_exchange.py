from binance.client import Client
from binance.exceptions import BinanceAPIException

time_frames = {'1m': Client.KLINE_INTERVAL_1MINUTE, '5m': Client.KLINE_INTERVAL_5MINUTE,
               '15m': Client.KLINE_INTERVAL_15MINUTE, '30m': Client.KLINE_INTERVAL_30MINUTE,
               '1h': Client.KLINE_INTERVAL_1HOUR, '2h': Client.KLINE_INTERVAL_2HOUR,
               '4h': Client.KLINE_INTERVAL_4HOUR, '6h': Client.KLINE_INTERVAL_6HOUR,
               '12h': Client.KLINE_INTERVAL_12HOUR, '1d': Client.KLINE_INTERVAL_1DAY,
               '1w': Client.KLINE_INTERVAL_1WEEK}


def get_client(apikey='', secret=''):
    client = Client(apikey, secret)
    return client
