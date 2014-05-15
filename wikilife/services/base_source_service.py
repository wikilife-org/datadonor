# coding=utf-8

from abc import abstractmethod
from django.conf import settings
from users.models import Profile
from utils.commons import send_email


class SourceServiceException(Exception):
    pass


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

    def _update_profile(self, user, **kwargs):
        if len(kwargs) == 0:
            return

        try:
            profile = Profile.objects.get(user=user)
            
            for field_name in kwargs:
                field_value = kwargs[field_name]
                field_source = getattr(profile, field_name+"_source")
                
                
                if field_value!=None and self._is_priority_source(field_source, self._profile_source):
                    setattr(profile, field_name, field_value)
                    if field_name == "email" and not profile.sent_welcome_email:
                        #send_email(field_value)
                    setattr(profile, field_name+"_source", self._profile_source)
    
            profile.save()
            return profile
        except:
            pass

    def _get_wikilife_token(self, user_id):
        profile = Profile.objects.get(user_id=user_id)
        return profile.wikilife_token

    def _ensure_wl_user(self, dd_user_profile):
        if not dd_user_profile.wikilife_ready:

            pin = "0000"
            gender = dd_user_profile.gender
            birthdate = dd_user_profile.date_of_birth
            height = dd_user_profile.height
            weight = dd_user_profile.weight
            device_id = dd_user_profile.device_id
            timezone = dd_user_profile.timezone
            city = dd_user_profile.city
            region = dd_user_profile.region
            country = dd_user_profile.country

            user_name = self._create_user_name(dd_user_profile.account_id) 

            success = self._wl_user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)

            if not success:
                raise SourceServiceException("Wikilife account creation failed for Datadonor dd_user_profile.account_id: %s" %dd_user_profile.account_id)

            oauth_token = self._wl_user_client.login(user_name, pin)
            dd_user_profile.wikilife_token = oauth_token
            dd_user_profile.wikilife_ready = True
            dd_user_profile.save()

        return dd_user_profile.wikilife_token

    def _create_user_name(self, unique_id):
        base_user_name = "dd_"
        user_name = "%s%s" %(base_user_name, unique_id)

        i = 1
        while not self._wl_user_client.check_name(user_name):
            user_name = "%s%s_$s" %(base_user_name, unique_id, i)
            i += 1

        return user_name

    def _send_logs_to_wl(self, dd_user_profile, wl_logs):
        #wl_token = self._ensure_wl_user(dd_user_profile)
        #self._wl_logs_client.add_logs(wl_token, wl_logs)
        pass

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
