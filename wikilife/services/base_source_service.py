# coding=utf-8

from abc import abstractmethod
from django.conf import settings
from users.models import Profile


class BaseSourceService(object):
    """
    Source referes to a user activity source, such a device (runkeeper, fitbit, etc), a social network (facebook, linkedin, etc) or other.
    """
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

    def _update_profile(self, user_id, **kwargs):
        if len(kwargs) == 0:
            return

        profile = Profile.objects.get(user_id=user_id)

        for field_name in kwargs:
            field_value = kwargs[field_name]
            field_source = getattr(profile, field_name+"_source")

            if field_value!=None and self._is_priority_source(field_source, self._profile_source):
                setattr(profile, field_name, field_value)
                setattr(profile, field_name+"_source", self._profile_source)

        profile.save()

        def _get_wikilife_token(self, user_id):
            profile = Profile.objects.get(user_id=user_id)
            return profile.wikilife_token

    @abstractmethod
    def pull_user_info(self, user_id, user_auth):
        """
        This method is called only once when the pipe is executed after the device authorization.
        Request using the source client
        Save local DD data

        :param user_id: Datadonor User ID.
        :type node: int

        :param user_auth: User Authenticantion info. Depends on source authentication type.
        :type node: dict

        :rtype: None
        """
        raise NotImplementedError()

    @abstractmethod
    def pull_user_activity(self, user_id, user_auth):
        """
        Request using the source client
        Save local DD data
        Send logs to WL

        :param user_id: Datadonor User ID.
        :type node: int

        :param user_auth: User Authenticantion info. Depends on source authentication type.
        :type node: dict

        :rtype: None
        """
        raise NotImplementedError()
