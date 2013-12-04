# coding=utf-8

from django.contrib.auth.models import User
from social.clients.foursquare import FoursquareClient
from social.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from social.models import SocialUserAggregatedData


FOURSQUARE_API = "https://api.foursquare.com/v2/"

NODE_ID_MAP = {
    "Running": 0, 
    "Cycling": 0, 
    "Mountain Biking": 0, 
    "Walking": 0, 
    "Hiking": 0, 
    "Downhill Skiing": 0, 
    "Cross-Country Skiing": 0, 
    "Snowboarding": 0, 
    "Skating": 0, 
    "Swimming": 0, 
    "Wheelchair": 0, 
    "Rowing": 0, 
    "Elliptical": 0, 
    "Other": 0
}


class FoursquareService(BaseDeviceService):

    _profile_source = "foursquare"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = FoursquareClient(FOURSQUARE_API, user_auth["access_token"])
        
        email = client.get_email()
        gender = client.get_gender()
        first_name = client.get_first_name()
        last_name = client.get_last_name()
        
        profile_items = {}
        
        if email:
            profile_items["email"] = email
        if first_name:
            profile_items["first_name"] = first_name
        if last_name:
            profile_items["last_name"] = last_name
        if gender:
            profile_items["gender"] = gender
            
        self._update_profile(user_id, **profile_items)
        
        friends_count = client.get_friends_count()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.foursquare_friends_count = friends_count
        aggregated.save()  

    def pull_user_activity(self, user_id, user_auth):
        wikilife_token = self._get_wikilife_token(user_id)
        client = FoursquareClient(FOURSQUARE_API, user_auth["access_token"])
        friends_count = client.get_friends_count()
        #Create logs to wikilife
        start_time = DateParser.from_datetime(item["start_time"])
        end_time = DateUtils.add_seconds(start_time, item["duration"])
        start = DateFormatter.to_datetime(start_time)
        end = DateFormatter.to_datetime(end_time)
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
        distance_km = item["total_distance"] * 1000
        calories = item["total_calories"]
        text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
        source = "datadonor.foursquare.%s" %item["source"]

        nodes = []
        nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
        nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

        log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
        self._log_client.add_log(wikilife_token, log)
