# coding=utf-8

from wikilife.client.base_wikilife_client import BaseWikilifeClient
from wikilife_utils.parsers.json_parser import JSONParser


class Stats(BaseWikilifeClient):

    def get_global_education_stats(self):
        response_body = self.rest_get("/4/stats/global/education/level/")[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto

    def get_global_work_stats(self):
        response_body = self.rest_get("/4/stats/global/work/experience/")[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto

    def get_global_social_stats(self):
        response_body = self.rest_get("/4/stats/global/social/")[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto