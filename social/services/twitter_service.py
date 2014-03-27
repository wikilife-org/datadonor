# coding=utf-8

from django.contrib.auth.models import User

from social.clients.twitter import TwitterClient
from social.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser

from social.models import SocialUserAggregatedData


TWITTER_API = "https://api.twitter.com/1.1/"

NODE_ID_MAP = {
}

class TwitterService(BaseDeviceService):

    _profile_source = "twitter"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = TwitterClient(TWITTER_API, user_auth["access_token"], user_auth["twitter_id"])
        
        followers = client.get_followers()
        tweets_last_week = client.get_tweets_last_week()
        retweets_last_week = client.get_retweets_last_week()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.twitter_followers_count = int(followers)
        aggregated.twitter_tweets_count_last_seven_days = tweets_last_week
        aggregated.twitter_retweets_count_last_seven_days = retweets_last_week
        aggregated.save()  

    def pull_user_activity(self, user_id, user_auth, twitter_id):
        pass
        """wikilife_token = self._get_wikilife_token(user_id)
        client = TwitterClient(user_auth["access_token"], twitter_id)
        followers = client.get_followers()
        tweets_last_week = client.get_tweets_last_week()
        retweets_last_week = client.get_retweets_last_week()
        #Create logs to wikilife
        start_time = DateParser.from_datetime(item["start_time"])
        end_time = DateUtils.add_seconds(start_time, item["duration"])
        start = DateFormatter.to_datetime(start_time)
        end = DateFormatter.to_datetime(end_time)
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
        distance_km = item["total_distance"] * 1000
        calories = item["total_calories"]
        text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
        source = "datadonor.twitter.%s" %item["source"]

        nodes = []
        nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
        nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

        log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
        self._log_client.add_log(wikilife_token, log)"""
