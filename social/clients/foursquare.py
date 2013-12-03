import requests
from social.clients.base_device_client import BaseDeviceClient

class FoursquareClient(BaseDeviceClient):

    _api_host = None
    _access_token = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token

 