# coding=utf-8

from wikilife.client.base_wikilife_client import BaseWikilifeClient
from wikilife_utils.parsers.json_parser import JSONParser


class Stats(BaseWikilifeClient):

    def check_name(self, user_name):
        params = {"name": user_name}
        response_body = self.rest_get("/4/user/check/", params)[2]
        dto = JSONParser.to_collection(response_body)
        return dto["available"]

    def get_account(self, oauth_token):
        params = {"oauth_token": oauth_token}
        response_body = self.rest_get("/4/user/account/", params)[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto
