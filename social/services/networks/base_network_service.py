# coding=utf-8

from abc import abstractmethod

class BaseNetworkService(object):
    
    #TODO name 
    #this replace pipe logic
    @abstractmethod
    def first_time(self):
        raise NotImplementedError()

    @abstractmethod
    def pull_from_network(self):
        raise NotImplementedError()
