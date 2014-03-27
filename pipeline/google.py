# coding=utf-8

from social.util.social_service_locator import SocialServiceLocator


def google_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "google":
        data = kwargs.get('response')
        social_user.extra_data["g_id"] = data["id"]
        social_user.save()
        dd_user_id = social_user.user.id
        google_service = SocialServiceLocator.get_instane().build_service_by_name("google")
        google_service.pull_user_info(dd_user_id, {"access_token": data["access_token"], "g_id":data["id"] })
        
 