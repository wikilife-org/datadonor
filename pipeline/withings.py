# coding=utf-8

from health.util.health_service_locator import HealthServiceLocator


def withings_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    
    if backend.name == "withings":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        #social_user.extra_data["twitter_id"] = data["id"]
        #social_user.save()
        withings_service = HealthServiceLocator.get_instane().build_service_by_name("withings")
        withings_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})

