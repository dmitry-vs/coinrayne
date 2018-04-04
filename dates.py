import datetime

date_seconds = '%Y-%m-%d %H:%M:%S'
date_minutes = '%Y-%m-%d %H:%M'


def currenttime():
    return datetime.datetime.now().strftime(date_seconds)


def fromtimestamp(timestamp, input_millisec=False, output_sec=False):
    dateformat = date_seconds if output_sec else date_minutes
    if input_millisec:
        timestamp /= 1000
    return datetime.datetime.fromtimestamp(timestamp).strftime(dateformat)
