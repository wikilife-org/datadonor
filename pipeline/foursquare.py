# coding=utf-8

from social.util.social_service_locator import SocialServiceLocator


def foursquare_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "foursquare":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        foursquare_service = SocialServiceLocator.get_instane().build_service_by_name("foursquare")
        foursquare_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})
