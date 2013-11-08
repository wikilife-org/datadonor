"""
Jawbone
"""
import requests
import json
from datetime import date
from time import time


from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list


def jawbone_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "jawbone":
        data = kwargs.get('response')
        jc = JawboneClient(data['access_token'])
        extra_data = jc.get_user_profile()
        print jc.get_user_trends(range_duration=5)
        print jc.get_user_workouts()
        print jc.get_user_sleep()
        print data
        
    
class JawboneClient():
    PAGE_SIZE = 25

    def __init__(self, access_token):
        self.api_host = 'https://jawbone.com/nudge/api/users/@me'
        self.headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % access_token}

    
    def make_api_call(self, url):
        res = requests.get(url , headers=self.headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data


    def date_formatter(self, date_obj):
        """format date to jawbone type int YYYYMMDD"""
        return date_obj.strftime('%Y%m%d')
    
    
    def get_params_url(self, params_dic):
        return "/?" + "&".join(["%s=%s" % (k, v) for k, v in params_dic.items()])


    def get_user_profile(self):
        url = self.api_host
        return self.make_api_call(url)


    def get_user_friends(self):
        url =  self.api_host + "/friends"       
        return self.make_api_call(url)


    def get_user_mood(self, date_obj=date.today()):
        mood_date = self.date_formatter(date_obj)
        url =  self.api_host + "/mood/?date=%d" % mood_date
        return self.make_api_call(url)
    
    
    def get_user_workouts(self, **kwargs):
        """
        date    int     Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        page_token    int     Timestamp used to paginate the list of workouts. The Developer must use the "next" link provided in the "links" section.
        start_time    int     To be used along with end_time. Epoch timestamp that denotes the start of the time range queried for events.
        end_time    int     To be used with start_time. Epoch timestamp that denotes the end of the time range queried for events.
        updated_after    int     Epoch timestamp to list events that are updated later than the timestamp. To be used with start_time to list events that were completed after said start_time.
        limit    int     Maximum number of results to return
        """
        if kwargs:
            if 'date' in kwargs.keys():
                kwargs['date'] =  self.date_formatter(kwargs['date'])

            params_url = self.get_params_url(kwargs)
        else:
            params_url = ''

        
        url = self.api_host + "/sleeps" + params_url
        return self.make_api_call(url)
        

    def get_user_sleep(self, **kwargs):
        """
        date int Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        page_token int Timestamp used to paginate the list of sleeps. The Developer must use the "next" link provided in the "links" section.
        start_time int To be used along with end_time. Epoch timestamp that denotes the start of the time range queried for events.
        end_time int To be used with start_time. Epoch timestamp that denotes the end of the time range queried for events.
        updated_after int Epoch timestamp to list events that are updated later than the timestamp. To be used with start_time to list events that were completed after said start_time.
        """
        if kwargs:
            if 'date' in kwargs.keys():
                kwargs['date'] =  self.date_formatter(kwargs['date'])
            params_url = self.get_params_url(kwargs)
        else:
            params_url = ''


        url = self.api_host + "/sleeps" + params_url
        return self.make_api_call(url)


    def get_user_trends(self, **kwargs):
        """
        end_date    int     Date, formatted as YYYYMMDD. If omitted, returns until today.
        range_duration    int     Used with range to determine how long to go back in time.
        range    string     Used with range_duration to determine how long to go back in time. Possible values are: d m
        bucket_size    string     Determines the granularity to use when aggregating the values. Possible values are: d w m y
        """
        if kwargs:
            if 'end_date' in kwargs.keys():
                kwargs['end_date'] =  self.date_formatter(kwargs['end_date'])
            params_url = self.get_params_url(kwargs)
        else:
            params_url = ""
        url =  self.api_host + "/trends" + params_url
        return self.make_api_call(url)
    

    def get_user_workouts(self):
        url =  self.api_host + "/workout"
        return self.make_api_call(url)
    
    
    def get_user_body_events(self):
        url =  self.api_host + "/body_events"
        return self.make_api_call(url)
    
    
    def get_user_cardiac_events(self):
        url =  self.api_host + "/cardiac_events"
        return self.make_api_call(url)
    
    
    def get_user_meals(self, **kwargs):
        """
        date    int  Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        page_token    int  Timestamp used to paginate the list of meals. The Developer must use the "next" link provided in the "links" section.
        start_time    int     To be used along with end_time. Epoch timestamp that denotes the start of the time range queried for events.
        end_time    int     To be used with start_time. Epoch timestamp that denotes the end of the time range queried for events.
        updated_after    int     Epoch timestamp to list events that are updated later than the timestamp. To be used with start_time to list events that were completed after said start_time.
        """
        if kwargs:
            if 'date' in kwargs.keys():
                kwargs['date'] =  self.date_formatter(kwargs['end_date'])
            params_url = self.get_params_url(kwargs)
        else:
            params_url = ""
            
        url =  self.api_host + "/meals" + params_url
        return self.make_api_call(url)