
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import time
import pytz
import math


def get_next_sunday_from_date(from_date):
    today = datetime.strptime(from_date, "%Y-%m-%d").date()
    offset = (today.weekday() - 6) % 7
    if offset ==0:
        offset = 7
    next_sunday = today + timedelta(days=offset)
    return (next_sunday, today.strftime("%Y-%m-%d"), next_sunday.strftime("%Y-%m-%d"))


def get_last_sunday_from_date(from_date):
    today = datetime.strptime(from_date, "%Y-%m-%d").date()
    offset = (today.weekday() - 6) % 7
    if offset ==0:
        offset = 7
    last_sunday = today - timedelta(days=offset)
    return (last_sunday, last_sunday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

def get_last_sunday():
    today = datetime.date.today()
    offset = (today.weekday() - 6) % 7
    if offset ==0:
        offset = 7
    last_sunday = today - timedelta(days=offset)
    return (last_sunday, last_sunday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

def get_last_year():
    today = datetime.date.today()
    last_year = today - timedelta(days=365)
    return (last_year, last_year.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

def get_last_sunday_list_days():
    today = datetime.date.today()
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
    today = datetime.date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        d_obj = {"date": e_day, "twitter_format": e_day.strftime("%a %b %d %Y")}
        result.append(d_obj)
    
    return result


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

def get_days_list_mili(days_count):
    result = []
    today = datetime.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append((e_day, unix_time_millis(e_day)))
    
    return result

def get_days_list(days_count):
    result = []
    today = datetime.date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append(e_day)
    
    return result

def get_days_list_int_tuple(days_count):
    result = []
    from_date = date(1970,01,01)
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append((e_day, (e_day- from_date).days))
    
    return result

def get_days_twitter(days_count):
    result = []
    today = date.today()
    for i in range(days_count):
        td = timedelta(days=i)
        e_day = today - td
        result.append(e_day.strftime("%a %b %d %Y"))
    
    return result




class DateUtils(object):

    @staticmethod
    def get_date(user_date):
        """
        TODO this method should not be here

        user_date: str
        Returns: date: "%Y-%m-%s" format
        """
        user_date = user_date[:19]
        date_obj = time.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        date_info = time.strftime("%Y-%m-%d", date_obj)

        return date_info

    @staticmethod
    def get_time(user_date):

        """
        TODO this method should not be here

        get_time

        params:
            user_date: str

        return:
                - time: "%H:%M:%S" format.
        """
        user_date = user_date[:19]
        date_obj = time.strptime(user_date, "%Y-%m-%d %H:%M:%S")
        time_info = time.strftime("%H:%M:%S", date_obj)

        return time_info

    @staticmethod
    def create_datetime(year, month, day, hour=0, minutes=0, sec=0):
        return datetime(year, month, day, hour, minutes, sec)

    @staticmethod
    def get_zero_datetime():
        return datetime(1, 1, 1)

    @staticmethod
    def get_date_utc():
        d = DateUtils.get_datetime_utc()
        return datetime(d.year, d.month, d.day)

    @staticmethod
    def get_datetime_utc():
        return datetime.utcnow()

    @staticmethod
    def get_datetime_local(tz_name):
        return datetime.now(pytz.timezone(tz_name))

    @staticmethod
    def get_utc_offset_str(tz_name):
        return datetime.now(pytz.timezone(tz_name)).strftime('%z')

    @staticmethod
    def to_datetime_utc(local_datetime):
        """
        local_date_value: Date with TZ. Naive dates will crash.
        """
        utc_datetime = local_datetime.astimezone(pytz.utc)
        return datetime(utc_datetime.year, utc_datetime.month, utc_datetime.day, utc_datetime.hour, utc_datetime.minute, utc_datetime.second, utc_datetime.microsecond)

    @staticmethod
    def add_seconds(date_value, seconds_offset):
        """
        date_value: Date
        seconds_offset: Integer
        """
        return date_value + relativedelta(seconds=seconds_offset)

    @staticmethod
    def add_days(date_value, days_offset):
        """
        date_value: Date
        days_offset: Integer
        """
        return date_value + relativedelta(days=days_offset)

    @staticmethod
    def add_months(date_value, months_offset):
        """
        date_value: Date
        months_offset: Integer
        """
        return date_value + relativedelta(months=months_offset)

    @staticmethod
    def equals_datetime(d1, d2, sec_error=0):
        """
        d1: Date
        d2: Date
        sec_error: Float
        """
        td = d1 - d2
        return math.fabs(td.total_seconds()) <= sec_error
    