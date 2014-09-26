import requests
from health.clients.base_device_client import BaseDeviceClient


class MoodsyClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _access_token = None
    _user_info = None
    _profile_id = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token
        
    def _get_resource(self, resource):
        if self._access_token is None:
            raise Exception("access_token cannot be None")

        headers = {'Authorization': 'Bearer %s' % self._access_token}
        url = "%s%s" % (self._api_host, resource)
        response = requests.get(
            url,
            headers=headers,
            verify=False,
        )

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_emotins(self):
        return self._get_resource("user/")
