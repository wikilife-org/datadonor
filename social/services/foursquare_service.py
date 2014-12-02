# coding=utf-8

from django.contrib.auth.models import User
from social.clients.foursquare import FoursquareClient
from social.models import SocialUserAggregatedData
from social.services.base_device_service import BaseDeviceService
from utils.date_util import DateUtils
#from wikilife_utils.logs.log_creator import LogCreator

FOURSQUARE_API = "https://api.foursquare.com/v2/"


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
            
        user = User.objects.get(id=user_id)
        dd_user_profile = self._update_profile(user, **profile_items)
        
        friends_count = client.get_friends_count()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.foursquare_friends_count = friends_count
        aggregated.save()

        """if created:
            start = DateUtils.get_datetime_utc()
            end = start
            text = "Foursquare"
            source = "datadonor.foursquare"
            nodes = []
            node_id = 278339

            metric_id = 278316
            value = friends_count 
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))

            wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
            self._send_logs_to_wl(dd_user_profile, [wl_log])"""

    def pull_user_activity(self, user_id, user_auth):
        pass
        """wikilife_token = self._get_wikilife_token(user_id)
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
        self._log_client.add_log(wikilife_token, log)"""
