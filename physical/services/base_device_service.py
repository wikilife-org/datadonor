# coding=utf-8

from abc import abstractmethod
from django.conf import settings


class BaseDeviceService(object):

    _profile_source = None

    _wl_user_client = None
    _wl_logs_client = None
    _wl_stats_client = None

    def __init__(self, wl_user_client, wl_logs_client, wl_stats_client):
        self._wl_user_client = wl_user_client
        self._wl_logs_client = wl_logs_client
        self._wl_stats_client = wl_stats_client

    def _is_priority_source(self, current_source, new_source):
        return current_source == None or settings.PROFILE_SOURCES_PRIORITY[current_source] > settings.PROFILE_SOURCES_PRIORITY[new_source]

    def _update_profile(self, **kwargs):
        profile = None

        for field_name in kwargs:
            field_value = kwargs[field_name]
            field_source = getattr(profile, field_name+"_source")

            if field_value!=None and self._is_priority_source(field_source, self._profile_source):
                setattr(profile, field_name, field_value)
                setattr(profile, field_name+"_source", self._profile_source)

        profile.save()

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
