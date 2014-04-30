
from health.util.health_service_locator import HealthServiceLocator


def ihealth_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "ihealth":
        data = kwargs.get('response')
        dd_user_id = request.user.id
        ihealth_service = HealthServiceLocator.get_instane().get_service_by_name("ihealth")
        ihealth_service.pull_user_info(dd_user_id, {"access_token": data["AccessToken"]})
        