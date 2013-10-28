# coding=utf-8

from abc import abstractmethod

class BaseSync(object):

    @abstractmethod
    def sync(self):
        pass