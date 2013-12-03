# coding=utf-8

from social.util.social_service_builder import SocialServiceBuilder

#TODO singletons sucks 

class SocialServiceLocator(object):
    __instance = None
    _service_builder = None
    _services = {}

    def __init__(self):
        if self.__instance != None:
            raise Exception("Singleton exception")

        self._service_builder = SocialServiceBuilder()

    @classmethod
    def get_instane(cls):
        if cls.__instance == None:
            cls.__instance = SocialServiceBuilder()

        return cls.__instance

    def get_service_by_name(self, service_name):
        if service_name not in self._services:
            self._services[service_name] = self._service_builder.build_service_by_name(service_name)

        return self._services[service_name]
