# coding=utf-8

from django.contrib.auth.models import User

from genomics.clients.twentythreeandme import TwentyThreeAndMeClient
from genomics.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser

from genomics.models import UserTrait, UserDrugResponse, UserRisk


TWENTY_THREE_AND_ME_API = "https://api.23andme.com/1/"

ACTIVITY_TYPE_NODE_ID_MAP = {
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

class TwentythreeandmeService(BaseDeviceService):

    _profile_source = "twentythreeandme"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = TwentyThreeAndMeClient(TWENTY_THREE_AND_ME_API, user_auth["access_token"])
        names = client.get_names()

        profile_items = {}

        if "first_name" in names:
            profile_items["first_name"] = names["first_name"]

        if "last_name" in names:
            profile_items["last_name"] = names["last_name"]

        self._update_profile(user_id, **profile_items)

        risks = client.get_risks()
        self._save_user_risks(user, risks)
        
        traits = client.get_traits()
        self._save_user_traits(user, traits)
        
        drug_responses = client.get_drug_responses()
        self._save_user_drug_responses(user, drug_responses)

    def _save_user_traits(self, user, traits):
        for trait in traits["traits"]:
            UserTrait.objects.create(user=user, report_id=trait["report_id"], value=trait["trait"])

    def _save_user_risks(self, user, risks):
        for risk in risks["risks"]:
            UserRisk.objects.create(user=user, report_id=risk["report_id"], value=risk["risk"])

    def _save_user_drug_responses(self, user, drug_responses):
        for drug_response in drug_responses["drug_responses"]:
            UserDrugResponse.objects.create(user=user, report_id=drug_response["report_id"], value=drug_response["status"])

    def pull_user_activity(self, user_id, user_auth):
        wikilife_token = self._get_wikilife_token(user_id)
        client = TwentyThreeAndMeClient(RUNKEEPER_API, user_auth["access_token"])
        fitness_activities = client.get_user_fitness_activities()
        self._log_fitness_activities(wikilife_token, fitness_activities["items"])
 
    def _log_fitness_activities(self, wikilife_token, items):
        for item in items:
            start_time = DateParser.from_datetime(item["start_time"])
            end_time = DateUtils.add_seconds(start_time, item["duration"])
            start = DateFormatter.to_datetime(start_time)
            end = DateFormatter.to_datetime(end_time)
            node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
            distance_km = item["total_distance"] * 1000
            calories = item["total_calories"]
            text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
            source = "datadonor.runkeeper.%s" %item["source"]

            nodes = []
            nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
            nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

            log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
            self._log_client.add_log(wikilife_token, log)
