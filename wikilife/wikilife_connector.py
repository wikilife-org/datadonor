# coding=utf-8

"""
authorize user
 obtain minimal DD user data
 
async
 sync DD users to WL
 sync global stats from WL
 
 pull device data
   send to WL via logs
   
"""

from physical.sync import PhysicalSync
from social.sync import SocialSync
from users.sync import UsersSync
from wikilife.util.wikilife_service_builder import WikilifeServiceBuilder


class WikilifeConnectorException(Exception):
    pass


class WikilifeConnector(object):

    _users_sync = None
    _social_sync = None
    _physical_sync = None

    def __init__(self):
        srv_bldr = WikilifeServiceBuilder()
        user_client = srv_bldr.build_user_client()
        stats_client = srv_bldr.build_stats_client()
        logs_client = srv_bldr.build_logs_client()

        self._users_sync = UsersSync(user_client)
        self._social_sync = SocialSync(logs_client, stats_client)
        self._physical_sync = PhysicalSync(stats_client)
    
    def sync(self):
        self._users_sync.sync()
        self._social_sync.sync()
        self._physical_sync.sync()
