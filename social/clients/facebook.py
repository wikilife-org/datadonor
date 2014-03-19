# coding=utf-8

import math
from utils.facebook import GraphAPI, GraphAPIError
from datetime import date, timedelta, datetime
from social.clients.base_device_client import BaseDeviceClient


class FacebookClient(BaseDeviceClient):

    _access_token = None
    _graph = None

    def __init__(self, access_token):
        self._access_token = access_token
        self._graph = GraphAPI(access_token)
    
    def get_profile(self):
        return self._graph.get_object("me")
    
    def get_avg_weekly_post(self):
        today = date.today()
        posts = self._graph.request("me/posts", {"limit":1000})
        index = len(posts["data"]) - 1
        initial_date = datetime.strptime(posts["data"][index]["created_time"][:10], "%Y-%m-%d").date()
        weeks = (today - initial_date).days / 7
        avg_posts = int(math.ceil((index + 1) / weeks))
        return avg_posts
    
    def get_avg_weekly_like(self):
        today = date.today()
        total_likes_query = "SELECT object_id FROM like WHERE user_id=me() limit 5000"
        total_likes = self._graph.fql(total_likes_query)
        count_likes = len(total_likes)
        index = count_likes - 1
        avg_likes = 0
        f_object = None
        
        while f_object is None and index >= 0:
            try:
                f_object = self._graph.get_object(total_likes[index]["object_id"])
            except GraphAPIError:
                index = index - 1
        
        if f_object:
            try:
                update_date = datetime.strptime(f_object["created_time"][:10], "%Y-%m-%d").date()
            except:
                update_date = datetime.strptime(f_object["updated_time"][:10], "%Y-%m-%d").date()
            weeks = ((today - update_date).days or 7) / 7
            if weeks>0:
                avg_likes = int(math.ceil((index + 1) / weeks))
        
        return avg_likes
    
    def get_friend_count(self):
        total_friend = self._graph.fql("SELECT friend_count FROM user WHERE uid = me()")[0]["friend_count"]
        return total_friend

 