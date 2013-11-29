import requests
from requests_oauthlib import OAuth1, OAuth1Session
import json
import datetime

from health.clients.base_device_client import BaseDeviceClient


class WithingsCredentials(object):
    def __init__(self, access_token=None, access_token_secret=None,
                 consumer_key=None, consumer_secret=None, user_id=None):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_id = user_id


class WithingsAuth(object):
    URL = 'https://oauth.withings.com/account'

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = None
        self.oauth_secret = None

    def get_authorize_url(self):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret)

        tokens = oauth.fetch_request_token('%s/request_token' % self.URL)
        self.oauth_token = tokens['oauth_token']
        self.oauth_secret = tokens['oauth_token_secret']

        return oauth.authorization_url('%s/authorize' % self.URL)

    def get_credentials(self, oauth_verifier):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.oauth_token,
                              resource_owner_secret=self.oauth_secret,
                              verifier=oauth_verifier)
        tokens = oauth.fetch_access_token('%s/access_token' % self.URL)
        return WithingsCredentials(access_token=tokens['oauth_token'],
                                   access_token_secret=tokens['oauth_token_secret'],
                                   consumer_key=self.consumer_key,
                                   consumer_secret=self.consumer_secret,
                                   user_id=tokens['userid'])

#Leer key, secret_key del settigs
# obtener token y token secret del user y user_id
# crear credentials en el init
class WithingsClient(BaseDeviceClient):
    URL = 'http://wbsapi.withings.net'
    
    _api_host = None
    _access_token = None
    _access_token_secret = None
    
    def __init__(self, credentials):
        self.credentials = credentials
        self.oauth = OAuth1(unicode(credentials.consumer_key),
                            unicode(credentials.consumer_secret),
                            unicode(credentials.access_token),
                            unicode(credentials.access_token_secret),
                            signature_type='query')
        self.client = requests.Session()
        self.client.auth = self.oauth
        self.client.params.update({'userid': credentials.user_id})

    def request(self, service, action, params=None, method='GET'):
        if params is None:
            params = {}
        params['action'] = action
        r = self.client.request(method, '%s/%s' % (self.URL, service), params=params)
        response = json.loads(r.content)
        if response['status'] != 0:
            raise Exception("Error code %s" % response['status'])
        return response.get('body', None)

    def get_user(self):
        return self.request('user', 'getbyuserid')

    def get_measures(self, **kwargs):
        r = self.request('measure', 'getmeas', kwargs)
        return WithingsMeasures(r)

    def subscribe(self, callback_url, comment, appli=1):
        params = {'callbackurl': callback_url,
                  'comment': comment,
                  'appli': appli}
        self.request('notify', 'subscribe', params)

    def unsubscribe(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        self.request('notify', 'revoke', params)

    def is_subscribed(self, callback_url, appli=1):
        params = {'callbackurl': callback_url, 'appli': appli}
        try:
            self.request('notify', 'get', params)
            return True
        except:
            return False

    def list_subscriptions(self, appli=1):
        r = self.request('notify', 'list', {'appli': appli})
        return r['profiles']


class WithingsMeasures(list):
    def __init__(self, data):
        super(WithingsMeasures, self).__init__([WithingsMeasureGroup(g) for g in data['measuregrps']])
        self.updatetime = datetime.datetime.fromtimestamp(data['updatetime'])


class WithingsMeasureGroup(object):
    MEASURE_TYPES = (('weight', 1), ('height', 4), ('fat_free_mass', 5),
                     ('fat_ratio', 6), ('fat_mass_weight', 8),
                     ('diastolic_blood_pressure', 9), ('systolic_blood_pressure', 10),
                     ('heart_pulse', 11))

    def __init__(self, data):
        self.data = data
        self.grpid = data['grpid']
        self.attrib = data['attrib']
        self.category = data['category']
        self.date = datetime.datetime.fromtimestamp(data['date'])
        self.measures = data['measures']
        for n, t in self.MEASURE_TYPES:
            self.__setattr__(n, self.get_measure(t))

    def is_ambiguous(self):
        return self.attrib == 1 or self.attrib == 4

    def is_measure(self):
        return self.category == 1

    def is_target(self):
        return self.category == 2

    def get_measure(self, measure_type):
        for m in self.measures:
            if m['type'] == measure_type:
                return m['value'] * pow(10, m['unit'])
        return None