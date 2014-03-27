from datetime import date, datetime, time, timedelta


def get_last_sunday():
    today = date.today()
    offset = (today.weekday() - 6) % 7
    if offset ==0:
        offset = 7
    last_sunday = today - timedelta(days=offset)
    return (last_sunday, last_sunday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

def get_last_sunday_list_days():
    today = date.today()
    offset = (today.weekday() - 6) % 7
    if offset ==0:
        offset = 7
    result = []
    for i in range(offset + 1):
        last_sunday = today - timedelta(days=i)
        result.append(last_sunday)
    return result

def get_days_list_completed(days_count):
    result = []
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        d_obj = {"date": e_day, "twitter_format": e_day.strftime("%a %b %d %Y")}
        result.append(d_obj)
    
    return result

def get_days_list(days_count):
    result = []
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append(e_day)
    
    return result

def get_days_twitter(days_count):
    result = []
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append(e_day.strftime("%a %b %d %Y"))
    
    return result
