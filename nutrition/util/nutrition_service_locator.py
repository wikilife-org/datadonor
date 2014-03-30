# coding=utf-8

from nutrition.util.nutrition_service_builder import NutritionServiceBuilder
from wikilife.util.wikilife_service_builder import WikilifeServiceBuilder

#TODO singletons sucks 

class NutritionServiceLocator(object):
    __instance = None
    _service_builder = None
    _services = {}

    def __init__(self):
        if self.__instance != None:
            raise Exception("Singleton exception")

        self._service_builder = NutritionServiceBuilder(WikilifeServiceBuilder())

    @classmethod
    def get_instane(cls):
        if cls.__instance == None:
            cls.__instance = NutritionServiceBuilder(WikilifeServiceBuilder())

        return cls.__instance

    def get_service_by_name(self, service_name):
        if service_name not in self._services:
            self._services[service_name] = self._service_builder.build_service_by_name(service_name)

        return self._services[service_name]