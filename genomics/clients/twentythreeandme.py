import requests


# leave these alone
BASE_URL = "https://api.23andme.com/1/"



class TwentyThreeAndMeClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _access_token = None
    _user_info = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token

    def _get_resource(self, resource):
        if self.access_token is None:
            raise Exception("access_token cannot be None")

        headers = {'Authorization': 'Bearer %s' % self.access_token}
        url = "%s%s" % (BASE_URL, resource)
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
            return response.text
        else:
            response.raise_for_status()

    def get_user(self):
        return self._get_resource("user/")

    def get_names(self):
        return self._get_resource("names/")

    def get_profiles(self):
        return self._get_resource("profiles/")

    def get_genotype(self, locations):
        return self._get_resource("genotypes/?locations=%s" % locations)
 