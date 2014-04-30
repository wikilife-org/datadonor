# coding=utf-8

from health.util.health_service_builder import HealthServiceBuilder

#TODO singletons sucks 

class HealthServiceLocator(object):
    __instance = None
    _service_builder = None
    _services = {}

    def __init__(self):
        if self.__instance != None:
            raise Exception("Singleton exception")

        self._service_builder = HealthServiceBuilder()

    @classmethod
    def get_instane(cls):
        if cls.__instance == None:
            cls.__instance = HealthServiceLocator()

        return cls.__instance

    def get_service_by_name(self, service_name):
        if service_name not in self._services:
            self._services[service_name] = self._service_builder.build_service_by_name(service_name)

        return self._services[service_name]