# coding=utf-8

from django.contrib.auth.models import User
from social.clients.google import GoogleClient
from social.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from social.models import SocialUserAggregatedData


GOOGLE_API = "https://www.googleapis.com/plus/v1/"

NODE_ID_MAP = {
}


class GoogleService(BaseDeviceService):

    _profile_source = "google"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = GoogleClient(GOOGLE_API, user_auth["access_token"],user_auth["g_id"])
        profile = client.get_profile()

        emails = profile.get("emails", [])
        gender = profile.get("gender", "")
        name = profile.get("name", {})
        
        profile_items = {}
        
        if emails:
            profile_items["email"] = emails[0]["value"]
            
        if gender:
            if gender =="male":
                gender = "m"
            elif gender == "female":
                gender = "f"
            profile_items["gender"] = gender
            
        if name:
            if "givenName" in name:
                profile_items["first_name"] = name["givenName"]
            if "familyName" in name:
                profile_items["last_name"] = name["familyName"]
            
        user = User.objects.get(id=user_id)
        self._update_profile(user, **profile_items)
        
        contacts_count = client.get_contacts_count()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.gplus_contacts_count = contacts_count
        aggregated.save()  

    def pull_user_activity(self, user_id, user_auth):
        pass
        """wikilife_token = self._get_wikilife_token(user_id)
        client = GoogleClient(GOOGLE_API, user_auth["access_token"], g_id)
        contacts_count = client.get_contacts_count()
        #Create logs to wikilife
        start_time = DateParser.from_datetime(item["start_time"])
        end_time = DateUtils.add_seconds(start_time, item["duration"])
        start = DateFormatter.to_datetime(start_time)
        end = DateFormatter.to_datetime(end_time)
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
        distance_km = item["total_distance"] * 1000
        calories = item["total_calories"]
        text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
        source = "datadonor.google.%s" %item["source"]

        nodes = []
        nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
        nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

        log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
        self._log_client.add_log(wikilife_token, log)"""
