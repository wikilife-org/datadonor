import requests
from physical.clients.base_device_client import BaseDeviceClient


class JawboneClient(BaseDeviceClient):
    def __init__(self, api_host, authorization_token):
        self.username = '@me'
        self.token = authorization_token
        self.auth_header = {'Authorization': 'Bearer %s' % self.token}
        self.content_header = {'Content-Type': 'multipart/form-data'}
        self.api_url_base = api_host


    # USER REQUESTS
    @property
    def user_request_url_base(self):
        return 'https://jawbone.com/nudge/api/v.1.1/users/%s' % self.username

    def get_user_information(self):
        user_information_request = requests.get(self.user_request_url_base, headers=self.auth_header)
        return user_information_request.json()

    def get_user_friends(self):
        user_friends_request = requests.get(self.user_request_url_base + '/friends', headers=self.auth_header)
        return user_friends_request.Response.json()

    def get_user_mood(self):
        user_mood_request = requests.get(self.user_request_url_base + '/mood', headers=self.auth_header)
        return user_mood_request.json()

    def get_user_trends(self):
        user_trends_request = requests.get(self.user_request_url_base + '/trend', headers=self.auth_header)
        return user_trends_request.json()

    def get_user_moves(self):
        user_moves_request = requests.get(self.user_request_url_base + '/moves', headers=self.auth_header)
        return user_moves_request.json()

    def get_user_workouts(self):
        user_workouts_request = requests.get(self.user_request_url_base + '/workouts', headers=self.auth_header)
        return user_workouts_request.json()

    def get_user_sleep_list(self):
        user_sleep_list_request = requests.get(self.user_request_url_base + '/sleeps', headers=self.auth_header)
        return user_sleep_list_request.json()

    def get_user_meals(self):
        user_sleep_list_request = requests.get(self.user_request_url_base + '/meals', headers=self.auth_header)
        return user_sleep_list_request.json()


    # MOVES
    def get_specific_move(self, move_xid):
        specific_move_request = requests.get(self.api_url_base + 'moves/' + '{%s}' % move_xid, headers=self.auth_header)
        return specific_move_request.json()

    def get_move_graphs(self, move_xid):
        move_graphs_request = requests.get(self.api_url_base + 'moves/' + '{%s}' + '/image' % move_xid, headers=self.auth_header)
        return move_graphs_request.json()

    def get_move_intensity(self, move_xid):
        move_intensity_request = requests.get(self.api_url_base + 'moves/' + '{%s}' + '/snapshot' % move_xid, headers=self.auth_header)
        return move_intensity_request.json()

    #  WORKOUTS
    def get_specific_workout(self, workout_xid):
        specific_workout_request = requests.get(self.api_url_base + 'workouts/' + '{%s}' % workout_xid, headers=self.auth_header)
        return specific_workout_request.json()

    def get_user_workout_graphs(self, workout_xid):
        workout_graphs_request = requests.get(self.api_url_base + 'workouts/' + '{%s}' + '/image' % workout_xid, headers=self.auth_header)
        return workout_graphs_request.json()

    def get_workout_intensity(self, workout_xid):
        workout_intensity_request = requests.get(self.api_url_base + 'workouts/' + '{%s}' + '/snapshot' % workout_xid, headers=self.auth_header)
        return workout_intensity_request.json()

    #SLEEP
    def get_specific_sleep(self, sleep_xid):
        specific_workout_request = requests.get(self.api_url_base + 'sleeps/' + '{%s}' % sleep_xid, headers=self.auth_header)
        return specific_workout_request.json()

    def get_user_workout_graphs(self, sleep_xid):
        sleep_graphs_request = requests.get(self.api_url_base + 'sleeps/' + '{%s}' + '/image' % sleep_xid, headers=self.auth_header)
        return sleep_graphs_request.json()

    def get_workout_intensity(self, sleep_xid):
        sleep_phases_request = requests.get(self.api_url_base + 'sleeps/' + '{%s}' + '/snapshot' % sleep_xid, headers=self.auth_header)
        return sleep_phases_request.json()

    #MEALS
    def get_specific_meal(self, meal_xid):
        specific_meal_request = requests.get(self.api_url_base + 'meals/' + '{%s}' % meal_xid, headers=self.auth_header)
        return specific_meal_request.json()

    def post_user_meal(self, meal):
        data = {'meal': meal}
        post_headers = dict(self.content_header.items() + self.auth_header.items())
        request_url = self.api_url_base + 'meals'
        user_meal_post = requests.post(request_url, data=data, headers=post_headers)
        return user_meal_post.text