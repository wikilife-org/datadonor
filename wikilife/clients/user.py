# coding=utf-8

from wikilife.clients.base_wikilife_client import BaseWikilifeClient
#from wikilife_utils.formatters.date_formatter import DateFormatter


class User(BaseWikilifeClient):

    def check_name(self, user_name):
        params = {"name": user_name}
        response_dto = self.rest_get("/4/user/check/", params)[2]
        return response_dto["available"]

    def login(self, user_name, pin):
        request_dto = {"userName": user_name, "pin": pin}
        response_dto = self.rest_post("/4/user/login/", request_dto)[2]
        return response_dto["oauth_token"]

    def edit_name(self, oauth_token, new_user_name):
        params = {"oauth_token": oauth_token}
        request_dto = {"newUserName": new_user_name}
        response_code = self.rest_post("/4/user/name/", request_dto, params, False)[0]
        return response_code == 200

    def edit_pin(self, oauth_token, new_pin):
        params = {"oauth_token": oauth_token}
        request_dto = {"newPin": new_pin}
        response_code = self.rest_post("/4/user/pin/", request_dto, params, False)[0]
        return response_code == 200

    def get_account(self, oauth_token):
        params = {"oauth_token": oauth_token}
        response_dto = self.rest_get("/4/user/account/", params)[2]
        return response_dto

    def create_account(self, user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country):
        request_dto = {
          "userName": user_name,
          "pin": pin,
          "gender": gender,
          "birthdate": birthdate,
          #"birthdate": DateFormatter.to_datetime(birthdate) if birthdate else birthdate,
          "height": height,
          "weight": weight,
          "deviceId": device_id,
          "timezone": timezone,
          "city": city,
          "region": region,
          "country": country,
        }
        
        #response_code = self.rest_post_account_creation("/4/user/account/", request_dto, False)
        response_code = self.rest_post("/4/user/account/", request_dto, False)[0]
        return response_code == 200

    def delete_account(self, oauth_token):
        params = {"oauth_token": oauth_token}
        response_code = self.rest_delete("/4/user/account/", params, False)[0]
        return response_code == 200
