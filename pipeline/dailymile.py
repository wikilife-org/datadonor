
from physical.util.physical_service_locator import PhysicalServiceLocator


def dailymile_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "dailymile":
        data = kwargs.get('response')
        dd_user_id = request.user.id
        runkeeper_service = PhysicalServiceLocator.get_instane().get_service_by_name("dailymile")
        runkeeper_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})
