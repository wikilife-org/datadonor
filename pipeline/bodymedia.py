"""
Bodymedia
"""

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list
import requests

def bodymedia_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "ihealth":
        data = kwargs.get('response')
        import pdb; pdb.set_trace()
        #fitbit_id = data["id"]
        #access_token = data["access_token"]
        #profile = get_user_profile(backend, access_token, fitbit_id)
        #result.update(profile["user"])
        #result["profile_img"] = result["avatar150"]
        #del result["avatar150"]
        #activity = get_user_activity(backend, access_token, fitbit_id)
        ##food = get_user_food(backend, access_token, fitbit_id)
        ##f_dict = dict(activity.items() + food.items())
        #result.update(activity)
        #social_user.extra_data.update(result)
        #social_user.save()

        return result