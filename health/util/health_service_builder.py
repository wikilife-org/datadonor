# coding=utf-8

from django.conf import settings
from wikilife.clients.logs import Logs
from wikilife.clients.stats import Stats
from wikilife.clients.user import User

SERVICES = {
    "withings": "health.services.withings_service.WithingsService",
    "moodpanda": "health.services.moodpanda_service.MoodPandaService",
    "ihealth": "health.services.ihealth_service.IhealthService",
    "moodsy": "health.services.moodsy_service.MoodsyService"
}


class HealthServiceBuilderException(Exception):
    pass


class HealthServiceBuilder(object):

    _wikilife_settings = None

    def __init__(self):
        self._wikilife_settings = settings.WIKILIFE

    def _build_wl_user_client(self):
        return User(self._wikilife_settings)

    def _build_wl_logs_client(self):
        return Logs(self._wikilife_settings)

    def _build_wl_stats_client(self):
        return Stats(self._wikilife_settings)

    def build_service_by_name(self, service_name):
        user_client = self._build_wl_user_client()
        logs_client = self._build_wl_logs_client()
        stats_client = self._build_wl_stats_client()

        if not service_name in SERVICES:
            raise PhysicalServiceBuilderException("Unknow service name '%s'" %service_name)

        class_fullname = SERVICES[service_name] 
        clazz = self._get_class(class_fullname)
        service = clazz(user_client, logs_client, stats_client)
        return service

    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )

        for comp in parts[1:]:
            m = getattr(m, comp)

        return m
