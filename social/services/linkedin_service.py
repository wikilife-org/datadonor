# coding=utf-8

from django.contrib.auth.models import User
from social.clients.linkedin import LinkedinClient
from social.models import SocialUserAggregatedData
from social.services.base_device_service import BaseDeviceService
from utils.date_util import DateUtils
#from wikilife_utils.logs.log_creator import LogCreator

LINKEDIN_API = "https://api.linkedin.com/v1/"


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
            
        user = User.objects.get(id=user_id)
        dd_user_profile = self._update_profile(user, **profile_items)
        
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
        
        """if created:
            wl_logs = []
            start = DateUtils.get_datetime_utc()
            end = start
            text = "Linkedin"
            source = "datadonor.linkedin"

            nodes = []
            node_id = 278340
            metric_id = 278329
            value = connections_count 
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
            wl_logs.append(wl_log)
            
            nodes = []
            node_id = 2
            metric_id = 278326
            value = education_level 
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
            wl_logs.append(wl_log)

            nodes = []
            node_id = 278333
            metric_id = 278323
            value = work_experince 
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
            wl_logs.append(wl_log)

            self._send_logs_to_wl(dd_user_profile, wl_logs)"""

    def pull_user_activity(self, user_id, user_auth):
        pass
        """wikilife_token = self._get_wikilife_token(user_id)
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
        self._log_client.add_log(wikilife_token, log)"""
