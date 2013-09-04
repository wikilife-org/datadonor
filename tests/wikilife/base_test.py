# coding=utf-8

import unittest
from wikilife.client.user import User


class BaseTest(unittest.TestCase):

    _clients = {}
    _settings = {
        "HOST": "http://localhost:7080"   
    }

    def get_settings(self):
        return self._settings

    def get_logger(self):
        return MockLogger()

    def get_user_client(self):
        if not "user" in self._clients:
            self._clients["user"] = User(self.get_logger(), self._settings)

        return self._clients["user"]


class MockLogger(object):

    def info(self, message):
        print message

    def error(self, message):
        print message
