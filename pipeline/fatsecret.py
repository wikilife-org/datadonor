
import requests
#from physical.util.physical_service_locator import PhysicalServiceLocator


def fatsecret_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "fatsecret":
        data = kwargs.get('response')
