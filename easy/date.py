from datetime import timedelta, datetime
import time

def datetimeIterator(from_date=datetime.now(), to_date=None, delta=timedelta(days=1)):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + delta
    return

def to_flot_time(dt):
    return float(time.mktime(dt.timetuple()))*1000
