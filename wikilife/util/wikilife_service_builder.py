# coding=utf-8

from django.conf import settings
from wikilife.clients.logs import Logs
from wikilife.clients.stats import Stats
from wikilife.clients.user import User


class WikilifeServiceBuilder(object):

    _wikilife_settings = None

    def __init__(self):
        self._wikilife_settings = settings.WIKILIFE

    def build_user_client(self):
        return User(self._wikilife_settings)

    def build_logs_client(self):
        return Logs(self._wikilife_settings)

    def build_stats_client(self):
        return Stats(self._wikilife_settings)
