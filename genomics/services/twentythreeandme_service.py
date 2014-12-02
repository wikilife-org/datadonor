# coding=utf-8

from django.contrib.auth.models import User

from genomics.clients.twentythreeandme import TwentyThreeAndMeClient
from genomics.services.base_device_service import BaseDeviceService
from utils.date_util import DateUtils
#from wikilife_utils.formatters.date_formatter import DateFormatter
#from wikilife_utils.logs.log_creator import LogCreator
#from wikilife_utils.parsers.date_parser import DateParser

from genomics.models import UserTrait, UserDrugResponse, UserRisk
from social_auth.db.django_models import UserSocialAuth


TWENTY_THREE_AND_ME_API = "https://api.23andme.com/1/"

REPORT_TYPE_NODE_ID_MAP = {
    "breastcancer": 0, 
    "gallstones": 0, 
    "atrialfib": 0, 
    "amd": 0, 
    "restlesslegs": 0, 
    "chronickidneydisease": 0, 
    "celiac": 0, 
    "scleroderma": 0, 
    "venousthromboembolism": 0, 
    "psoriasis":0,
    "melanoma":0,
    "glaucoma":0,
    "multiplesclerosis":0,
    "crohns":0,
    "escc":0,
    "gca":0,
    "obesity":0,
    "coronaryheartdisease":0,
    "type2diabetes":0,
    "lungcancer": 0, 
    "colorectalcancer": 0, 
    "rheumarthritis": 0, 
    "type1diabetes": 0, 
    "uc": 0,
    "primary_biliary_cirrhosis": 0,
    "lupus": 0,
    "bipolar_disorder": 0,
    "prostate":0
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
        
        user = User.objects.get(id=user_id)
        self._update_profile(user, **profile_items)
        

        risks = client.get_risks()
        self._save_user_risks(user, risks)
        
        traits = client.get_traits()
        self._save_user_traits(user, traits)
        
        drug_responses = client.get_drug_responses()
        self._save_user_drug_responses(user, drug_responses)

        

    def _save_user_traits(self, user, traits):
        for trait in traits["traits"]:
            #UserTrait.objects.create(user=user, report_id=trait["report_id"], value=trait["trait"])
            UserTrait.objects.get_or_create(user=user, report_id=trait["report_id"], value=trait["trait"])

    def _save_user_risks(self, user, risks):
        for risk in risks["risks"]:
            #UserRisk.objects.create(user=user, report_id=risk["report_id"], value=risk["risk"], population_risk=risk["population_risk"])
            UserRisk.objects.get_or_create(user=user, report_id=risk["report_id"], value=risk["risk"], population_risk=risk["population_risk"])

    def _save_user_drug_responses(self, user, drug_responses):
        for drug_response in drug_responses["drug_responses"]:
            #UserDrugResponse.objects.create(user=user, report_id=drug_response["report_id"], value=drug_response["status"])
            UserDrugResponse.objects.get_or_create(user=user, report_id=drug_response["report_id"], value=drug_response["status"])

    def pull_user_activity(self, user_id, user_auth):
        pass
    """   
     def pull_user_activity(self, user_id, user_auth):
        wikilife_token = self._get_wikilife_token(user_id)
        client = TwentyThreeAndMeClient(TWENTY_THREE_AND_ME_API, user_auth["access_token"])

        risks = client.get_risks()
        self._log_genomics_risks(user, risks)
        
        traits = client.get_traits()
        self._log_genomics_traits(user, traits)
        
        drug_responses = client.get_drug_responses()
        self._log_genomics_drug_responses(user, drug_responses)
 
    def _log_genomics_risks(self, wikilife_token, items):
        for item in items["risks"]:
            start_time = DateParser.from_datetime(item["start_time"])
            end_time = DateUtils.add_seconds(start_time, item["duration"])
            start = DateFormatter.to_datetime(start_time)
            end = DateFormatter.to_datetime(end_time)
            node_id = REPORT_TYPE_NODE_ID_MAP[item["report_id"]]
            distance_km = item["total_distance"] * 1000
            calories = item["total_calories"]
            text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
            source = "datasharing.23andme.%s" %item["source"]

            nodes = []
            nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))

            log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
            self._log_client.add_log(wikilife_token, log)

    def _log_genomics_traits(self, wikilife_token, items):
        for item in items["traits"]:
            start_time = DateParser.from_datetime(item["start_time"])
            end_time = DateUtils.add_seconds(start_time, item["duration"])
            start = DateFormatter.to_datetime(start_time)
            end = DateFormatter.to_datetime(end_time)
            node_id = REPORT_TYPE_NODE_ID_MAP[item["report_id"]]
            distance_km = item["total_distance"] * 1000
            calories = item["total_calories"]
            text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
            source = "datasharing.23andme.%s" %item["source"]

            nodes = []
            nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
            nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

            log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
            self._log_client.add_log(wikilife_token, log)

    def _log_genomics_drug_responses(self, wikilife_token, items):
        for item in items["drug_responses"]:
            
            start_time = DateParser.from_datetime(item["start_time"])
            end_time = DateUtils.add_seconds(start_time, item["duration"])
            start = DateFormatter.to_datetime(start_time)
            end = DateFormatter.to_datetime(end_time)
            
            node_id = REPORT_TYPE_NODE_ID_MAP[item["report_id"]]
            description = item["description"]
            status = item["status"]
            text = "%s %s" %(description, status)
            source = "datasharing.23andme"

            nodes = []
            nodes.append(LogCreator.create_log_node(self, node_id, 0, status))

            log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
            self._log_client.add_log(wikilife_token, log)"""
            