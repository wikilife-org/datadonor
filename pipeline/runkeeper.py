"""
Runkeeper
"""

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list
import requests

def runkeeper_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "runkeeper":
        data = kwargs.get('response')
        rk_id = data["id"]
        print
