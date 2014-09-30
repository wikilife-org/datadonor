# coding=utf-8
import requests


#MOODSY_API = 'http://api.moodsy.me/'
MOODSY_API = 'http://live.moodsy.me:7080/'


class MoodsyOAuthClient(object):
    pass

class MoodsyClient(object):
    PAGE_SIZE = 25

    _api_host = MOODSY_API
    _access_token = None
    _user_info = None
    _profile_id = None

    def __init__(self, access_token):
        self._access_token = access_token
        
    def _get_resource(self, resource):
        if self._access_token is None:
            raise Exception("access_token cannot be None")

        url = "%s%s?token=%s" % (self._api_host, resource, self._access_token)
        response = requests.get(
            url,
            verify=False,
        )

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_emotions(self):
        params = {"to": None }
        return self._get_resource("timeline/me/")

    def get_profile(self):
        params = {"to": None }
        return self._get_resource("timeline/me/")
    
    def get_mood_stats(self):
        params = {"to": None }
        return self._get_resource("timeline/me/")
    
    def get_people_stats(self):
        params = {"to": None }
        return self._get_resource("timeline/me/")

    def get_place_stats(self):
        params = {"to": None }
        return self._get_resource("timeline/me/")
    

if __name__ == "__main__":
    token = "27tn8sjbvahflf1ktp"
    api = MoodsyClient(token)
    emotions =  api.get_emotions()
    print emotions
    
