# coding=utf-8

from django.contrib.auth.models import User
from social.clients.linkedin import LinkedinClient
from social.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from social.models import SocialUserAggregatedData


LINKEDIN_API = "https://api.linkedin.com/v1/"

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


class LinkedinService(BaseDeviceService):

    _profile_source = "linkedin"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = LinkedinClient(LINKEDIN_API, user_auth["access_token"])
        profile = client.get_profile()

        email = profile.get("emailAddress", "")
        first_name = profile.get("firstName", "")
        last_name = profile.get("lastName", "")
        
        profile_items = {}
        
        if email:
            profile_items["email"] = email
        if first_name:
            profile_items["first_name"] = first_name
        if last_name:
            profile_items["last_name"] = last_name
            
        self._update_profile(user_id, **profile_items)
        
        connections_count = client.get_connections_count()
        education_level, degree = client.get_education_level()
        work_experince = client.get_work_experience_years()

        aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
        aggregated.user = user
        aggregated.linkedin_connections_count = connections_count
        aggregated.work_experience_years = work_experince
        aggregated.education_level = education_level
        aggregated.education_degree = degree
        aggregated.save()  

    def pull_user_activity(self, user_id, user_auth):
        wikilife_token = self._get_wikilife_token(user_id)
        client = LinkedinClient(LINKEDIN_API, user_auth["access_token"])
        connections_count = client.get_connections_count()
        education_level, degree = client.get_education_level()
        work_experince = client.get_work_experience_years()
        #Create logs to wikilife
        start_time = DateParser.from_datetime(item["start_time"])
        end_time = DateUtils.add_seconds(start_time, item["duration"])
        start = DateFormatter.to_datetime(start_time)
        end = DateFormatter.to_datetime(end_time)
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
        distance_km = item["total_distance"] * 1000
        calories = item["total_calories"]
        text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
        source = "datadonor.linkedin.%s" %item["source"]

        nodes = []
        nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
        nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

        log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
        self._log_client.add_log(wikilife_token, log)
