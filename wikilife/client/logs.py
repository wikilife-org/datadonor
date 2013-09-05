# coding=utf-8

from wikilife.client.base_wikilife_client import BaseWikilifeClient
from wikilife_utils.parsers.json_parser import JSONParser


class Logs(BaseWikilifeClient):

    def add_logs(self, oauth_token, logs):
        params = {"oauth_token": oauth_token}
        request_dto = logs
        request_body = JSONParser.to_json(request_dto)
        response_code = self.rest_post("/4/logs/", request_body, params)[0]
        return response_code == 200
