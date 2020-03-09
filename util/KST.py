import datetime
from pytz import timezone, utc

def kst_time():
    kst = timezone('Asia/Seoul')
    now = datetime.datetime.utcnow()
    utc.localize(now)
    kst.localize(now)
    return utc.localize(now).astimezone(kst).strftime("%Y-%m-%d %H:%M:%S")

def kst_time_for_file():
    kst = timezone('Asia/Seoul')
    now = datetime.datetime.utcnow()
    utc.localize(now)
    kst.localize(now)
    return utc.localize(now).astimezone(kst).strftime("%Y-%m-%d %Hh%Mm")