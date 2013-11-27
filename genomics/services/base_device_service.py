# coding=utf-8

from abc import abstractmethod
from wikilife.services.base_source_service import BaseSourceService


class BaseDeviceService(BaseSourceService):

    _wl_user_client = None
    _wl_logs_client = None
    _wl_stats_client = None

    def __init__(self, wl_user_client, wl_logs_client, wl_stats_client):
        self._wl_user_client = wl_user_client
        self._wl_logs_client = wl_logs_client
        self._wl_stats_client = wl_stats_client

    @abstractmethod
    def pull_user_info(self, user_auth):
        """
        This method is called only once when the pipe is executed after the device authorization.
        Request using the device client
        Save local DD data

        :param user_auth: User Authenticantion info. Depends on device authentication type.
        :type node: dict

        :rtype: None
        """
        raise NotImplementedError()

    @abstractmethod
    def pull_user_activity(self, user_auth):
        """
        Request using the device client
        Save local DD data
        Send logs to WL

        :param user_auth: User Authenticantion info. Depends on device authentication type.
        :type node: dict

        :rtype: None
        """
        raise NotImplementedError()
