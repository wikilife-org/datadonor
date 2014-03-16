import requests
from genomics.clients.base_device_client import BaseDeviceClient


class TwentyThreeAndMeClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _access_token = None
    _user_info = None
    _profile_id = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token
        self._profile_id = self.get_user()["profiles"][0]["id"]
        
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
        print "url: %s" % url
        print "response: %s" % response
        print "response.json: %s" % response.json()
        print "response.text: %s" % response.text
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_user(self):
        return self._get_resource("user/")

    def get_names(self):
        return self._get_resource("names/%s/"%self._profile_id)

    def get_genotype(self, locations):
        return self._get_resource("genotypes/?locations=%s" % locations)
    
    def get_risks(self):
        return self._get_resource("risks/%s/"%self._profile_id)
    
    def get_drug_responses(self):
        return self._get_resource("drug_responses/%s/"%self._profile_id)

    def get_traits(self):
        return self._get_resource("traits/%s/"%self._profile_id)
 