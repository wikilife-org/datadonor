
import requests
from nutrition.util.nutrition_service_locator import NutritionServiceLocator


def fatsecret_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "fatsecret":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        #social_user.extra_data["twitter_id"] = data["id"]
        #social_user.save()
        fatsecret_service = NutritionServiceLocator.get_instane().build_service_by_name("fatsecret")
        fatsecret_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})

