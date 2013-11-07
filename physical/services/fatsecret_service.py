# coding=utf-8

from physical.services.base_device_service import BaseDeviceService


class FatsecretService(BaseDeviceService):

    _profile_source = "fatsecret"

    def pull_user_info(self, user_id, user_auth):
        pass

    def pull_user_activity(self, user_id, user_auth):
        pass
