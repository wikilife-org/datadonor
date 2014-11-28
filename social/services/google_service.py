# coding=utf-8

from django.contrib.auth.models import User
from social.clients.google import GoogleClient
from social.models import SocialUserAggregatedData
from social.services.base_device_service import BaseDeviceService
from utils.date_util import DateUtils
from wikilife_utils.logs.log_creator import LogCreator

GOOGLE_API = "https://www.googleapis.com/plus/v1/"


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
        dd_user_profile = self._update_profile(user, **profile_items)
        
        contacts_count = client.get_contacts_count()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.gplus_contacts_count = contacts_count
        aggregated.save()  

        if created:
            start = DateUtils.get_datetime_utc()
            end = start
            text = "Foursquare"
            source = "datadonor.google"
            nodes = []
            node_id = 278338

            metric_id = 278318
            value = contacts_count 
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))

            wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
            self._send_logs_to_wl(dd_user_profile, [wl_log])

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
