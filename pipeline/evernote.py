
from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request


def evernote_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "evernote":
        data = kwargs.get('response')

        result.update(data)
        return result
