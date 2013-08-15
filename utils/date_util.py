from datetime import date, datetime, time, timedelta

def get_days_list(days_count):
    result = []
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        result.append(today - td)
    
    return result