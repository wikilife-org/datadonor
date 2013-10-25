# coding=utf-8

from wikilife.clients.base_wikilife_client import BaseWikilifeClient


class Logs(BaseWikilifeClient):

    def add_logs(self, oauth_token, logs):
        params = {"oauth_token": oauth_token}
        request_dto = logs
        response_code = self.rest_post("/4/logs/", request_dto, params, False)[0]
        return response_code == 200
