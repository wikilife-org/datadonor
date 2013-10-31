# coding=utf-8

import unittest
from health.clients.mood_panda import MoodPandaClient

class MoodPandaClientTest(unittest.TestCase):
    _user_email = "joako84@gmail.com"
    _api_host = "http://moodpanda.com/api/"
    _api_key = "b88cc222-216c-47d2-9577-829e3ea662ac"
    
    def test_missing_paramenters(self):
        #self.assertRaises(Exception, MoodPandaClient(self._api_host, self._api_key))
        try:
            MoodPandaClient(self._api_host, self._api_key)
            assert False
        except Exception, e:
            assert True
    
    def test_get_user_id(self):
        mood_panda_client = MoodPandaClient(self._api_host, self._api_key, self._user_email)
        assert mood_panda_client._user_id == "7563872"
        mood_panda_client = MoodPandaClient(self._api_host, self._api_key, "jquintas@wikilife.org")
        assert mood_panda_client._user_id == ""
        
    def test_get_user_profile(self):
        mood_panda_client = MoodPandaClient(self._api_host, self._api_key, self._user_email)
        profile = mood_panda_client._get_user_profile()
        assert profile != None
        
    def test_get_user_mood_last_30_days(self):
        mood_panda_client = MoodPandaClient(self._api_host, self._api_key, self._user_email)
        moods = mood_panda_client._get_user_mood_last_30_days()
        print moods
    
if __name__ == '__main__':
    unittest.main()
