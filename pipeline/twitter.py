# coding=utf-8

from social.util.social_service_locator import SocialServiceLocator


def twitter_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    
    if backend.name == "twitter":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        twitter_id = data["id"]
        twitter_service = SocialServiceLocator.get_instane().build_service_by_name("twitter")
        twitter_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]}, twitter_id)
