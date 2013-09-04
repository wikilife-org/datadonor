# coding=utf-8

from wikilife.client.base_wikilife_client import BaseWikilifeClient
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.parsers.json_parser import JSONParser


class User(BaseWikilifeClient):

    def check_name(self, user_name):
        params = {"name": user_name}
        response_body = self.rest_get("/4/user/check/", params)[2]
        dto = JSONParser.to_collection(response_body)
        return dto["available"]

    def login(self, user_name, pin):
        request_dto = {"userName": user_name, "pin": pin}
        request_body = JSONParser.to_json(request_dto)
        response_body = self.rest_post("/4/user/login/", request_body)[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto["oauth_token"]

    def edit_name(self, oauth_token, new_user_name):
        params = {"oauth_token": oauth_token}
        request_dto = {"newUserName": new_user_name}
        request_body = JSONParser.to_json(request_dto)
        response_code = self.rest_post("/4/user/name/", request_body, params)[0]
        return response_code == 200

    def edit_pin(self, oauth_token, new_pin):
        params = {"oauth_token": oauth_token}
        request_dto = {"newPin": new_pin}
        request_body = JSONParser.to_json(request_dto)
        response_code = self.rest_post("/4/user/pin/", request_body, params)[0]
        return response_code == 200

    def get_account(self, oauth_token):
        params = {"oauth_token": oauth_token}
        response_body = self.rest_get("/4/user/account/", params)[2]
        response_dto = JSONParser.to_collection(response_body)
        return response_dto

    def create_account(self, user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country):
        dto = {
          "userName": user_name,
          "pin": pin,
          "gender": gender,
          "birthdate": DateFormatter.to_datetime(birthdate),
          "height": height,
          "weight": weight,
          "deviceId": device_id,
          "timezone": timezone,
          "city": city,
          "region": region,
          "country": country
        }
        body = JSONParser.to_json(dto)
        response_code = self.rest_post("/4/user/account/", body)[0]
        return response_code == 200

    def delete_account(self, oauth_token):
        params = {"oauth_token": oauth_token}
        response_code = self.rest_delete("/4/user/account/", params)[0]
        return response_code == 200
