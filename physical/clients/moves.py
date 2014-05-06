# A python class for easy access to the Moves App data. Created by Joost Plattel [http://github.com/jplattel]

import requests
from datetime import date, datetime, time, timedelta


class MovesClient():
    def __init__(self, api_url, token):
        self.token = token # Callback URL for getting an access token
        self.api_url = api_url
        self.user_profile = self.get_profile()
    
    # Base request
    def get(self, token, endpoint):
        token = '&access_token=' + token
        return requests.get(self.api_url + endpoint + token).json()
    
    # /user/profile
    def get_profile(self):
        token = '?access_token=' + self.token
        root = '/user/profile'
        return requests.get(self.api_url + root + token).json()
    
    # Summary requests
    
    # /user/summary/daily/<date>
    # /user/summary/daily/<week>
    # /user/summary/daily/<month>
    def get_summary(self, token, date):
        token = '?access_token=' + token
        return requests.get(self.api_url + '/user/summary' + date + token).json()
    
    
    # Range requests, max range of 7 days!
    
    # /user/summary/daily?from=<start>&to=<end>
    # /user/activities/daily?from=<start>&to=<end>
    # /user/places/daily?from=<start>&to=<end>
    # /user/storyline/daily?from=<start>&to=<end>
    def get_range(self, endpoint, start, end):
        export = self.get(self.token, endpoint + '?from=' + start + '&to=' + end)
        return export
    
    def get_activities(self):

        first_date = datetime.strptime(self.user_profile["profile"]["firstDate"], "%Y%m%d").date()
        
        if (date.today() - first_date).days > 7:
            today = date.today().strftime("%Y%m%d")
            delta_date = timedelta(days=10)
            from_date = (date.today() - delta_date).strftime("%Y%m%d")
        else:
            from_date = first_date.strftime("%Y%m%d")
        return self.get_range("/user/activities/daily", from_date, today)
    
    def get_places(self):
        today = date.today().strftime("%Y-%m-%d")
        from_date = timedelta(days=-31).strftime("%Y-%m-%d")
        
        return get_range("/user/places", from_date, today)

    def get_storyline(self):
        today = date.today().strftime("%Y-%m-%d")
        from_date = timedelta(days=-31).strftime("%Y-%m-%d")
        
        return get_range("/user/storyline", from_date, today)
    