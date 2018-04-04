import argparse


def parse_args_main_runonce():
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
    args.start_date += ' UTC+3'
    args.end_date += ' UTC+3'

    return args


def parse_args_main_runloop():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file', type=str, default='coins.xml',
                        help='text file with coin parameters, default is coins.xml')
    parser.add_argument('-o', dest='output_file', type=str, default='',
                        help='output file, default is trades_currenttime')

    args = parser.parse_args()
    return args
