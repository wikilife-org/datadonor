# coding=utf-8

from users.models import Profile
from wikilife.base_sync import BaseSync


class UsersSyncException(Exception):
    pass


class UsersSync(BaseSync):
    
    _user_client = None
    
    def __init__(self, user_client):
        self._user_client = user_client

    def sync(self):
        self._push_new_users_to_wl()
        #TODO pull user account changes from WL

    def _push_new_users_to_wl(self):
        for profile in Profile.objects.filter(wikilife_token=None):
            user_name = self._create_user_name(profile.account_id)
            pin = "0000"
            gender = profile.gender
            birthdate = profile.date_of_birth
            height = None
            weight = None
            device_id = None
            timezone = None
            city = None
            region = None
            country = None
            success = self._user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)

            if not success:
                raise UsersSyncException("Wikilife account creation failed for Datadonor profile.account_id: %s" %profile.account_id)

            token = self._user_client.login(user_name, pin)
            profile.wikilife_token = token
            profile.save()

    def _create_user_name(self, unique_id):
        base_user_name = "datadonor_"
        user_name = "%s%s" %(base_user_name, unique_id)

        i = 1
        while not self._user_client.check_name(user_name):
            user_name = "%s%s_$s" %(base_user_name, unique_id, i)
            i += 1

        return user_name