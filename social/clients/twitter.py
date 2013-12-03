# coding=utf-8

from social.clients.base_device_client import BaseDeviceClient
from django.utils import simplejson
from utils.client import dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_twitter


class TwitterClient(BaseDeviceClient):

    _api_host = None
    _access_token = None
    _timeline = None
    _profile = None
    
    def __init__(self, api_host, access_token, user_id):
        self._api_host = api_host
        self._access_token = access_token
        self._user_id = user_id
        self._timeline = self.get_user_timeline()
        self._profile = self.get_profile()

    def get_profile(self):
        if self._profile:
            return self._profile
        url = "users/show.json?user_id=%s"%self._user_id
        self._profile = self._get_resource(url)
        return self._profile
    
    def get_follows(self):
        return self._profile["friends_count"]
    
    def get_followers(self):
        return self._profile["followers_count"]
    
    def get_tweets_count(self):
        return self._profile["tweets_count"]
    
    def get_tweets_last_week(self):
        if not self._timeline:
            self._timeline = self.get_user_timeline()
        day_list = get_days_twitter(7)
        
        twitter_tweets_count_last_seven_days = 0
        
        for tweet in self._timeline:
            tweet_date = "{0} {1}".format(tweet["created_at"][:10], tweet["created_at"][26:])
            if tweet_date in day_list:
                if not "RT @" in tweet["text"]:
                    twitter_tweets_count_last_seven_days = twitter_tweets_count_last_seven_days + 1
        return twitter_tweets_count_last_seven_days
    
    def get_retweets_last_week(self):
        if not self._timeline:
            self._timeline =  self.get_user_timeline()

        day_list = get_days_twitter(7)
        
        twitter_retweets_count_last_seven_days = 0
        
        for tweet in self._timeline:
            tweet_date = "{0} {1}".format(tweet["created_at"][:10], tweet["created_at"][26:])
            if tweet_date in day_list:
                if "RT @" in tweet["text"]:
                    twitter_retweets_count_last_seven_days = twitter_retweets_count_last_seven_days + 1
        return twitter_retweets_count_last_seven_days
    
    def get_user_timeline(self):
        url = "statuses/user_timeline.json?exclude_replies=false&include_rts=true&trim_user=true"
        return self._get_resource(url)
 
 
    def _get_resource(self, url):
        request_url = self._api_host + url
        request = build_consumer_oauth_request("twitter",self._access_token, request_url)
        response = '\n'.join(dsa_urlopen(request.to_url()).readlines())
        response = simplejson.loads(response)
        return response
    