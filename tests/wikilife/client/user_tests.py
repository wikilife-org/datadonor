# coding=utf-8

from tests.wikilife.base_test import BaseTest
from utils.date_util import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter


class UserTests(BaseTest):

    def NO_test_check_user_name_availability(self):
        user_name = "TEST_qwerty123"
        user_client = self.get_user_client()
        available = user_client.check_name(user_name)
        self.assertTrue(available)

    def NO_test_create_account(self):
        user_name = "TEST_qwerty2_1240"
        pin = "1234"
        gender = "Male"
        birthdate = DateUtils.create_datetime(1980, 1, 1, 12, 30, 45)
        height = 1.8
        weight = 75
        device_id = "test_device_id"
        timezone = "America/Argentina/Buenos_Aires"
        city = "Buenos Aires"
        region = "Buenos Aires"
        country = "Argentina"

        user_client = self.get_user_client()
        success = user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)
        self.assertTrue(success)

    def NO_test_login(self):
        user_name = "TEST_qwerty2_22353"
        pin = "1234"
        gender = "Male"
        birthdate = DateUtils.create_datetime(1980, 1, 1, 12, 30, 45)
        height = 1.8
        weight = 75
        device_id = "test_device_id"
        timezone = "America/Argentina/Buenos_Aires"
        city = "Buenos Aires"
        region = "Buenos Aires"
        country = "Argentina"

        user_client = self.get_user_client()
        user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)

        oauth_token = user_client.login(user_name, pin)
        assert oauth_token != None

    def NO_test_get_account(self):
        user_name = "TEST_qwerty2_323468"
        pin = "1234"
        gender = "Male"
        birthdate = DateUtils.create_datetime(1980, 1, 1, 12, 30, 45)
        height = 1.8
        weight = 75
        device_id = "test_device_id"
        timezone = "America/Argentina/Buenos_Aires"
        city = "Buenos Aires"
        region = "Buenos Aires"
        country = "Argentina"

        user_client = self.get_user_client()
        user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)
        oauth_token = user_client.login(user_name, pin)

        expected = {
          "userName": user_name,
          "status": 1,
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

        user_account = user_client.get_account(oauth_token)
        self.assertDictEqual(user_account, expected)

    def NO_test_delete_account(self):
        user_name = "TEST_qwerty2_4234568"
        pin = "1234"
        gender = "Male"
        birthdate = DateUtils.create_datetime(1980, 1, 1, 12, 30, 45)
        height = 1.8
        weight = 75
        device_id = "test_device_id"
        timezone = "America/Argentina/Buenos_Aires"
        city = "Buenos Aires"
        region = "Buenos Aires"
        country = "Argentina"

        user_client = self.get_user_client()
        user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)
        oauth_token = user_client.login(user_name, pin)

        success = user_client.delete_account(oauth_token)
        self.assertTrue(success)
