
import requests
from health.util.health_service_locator import HealthServiceLocator


def withings_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "withings":
        data = kwargs.get('response')
        #Llmar al client
        #Enviar los datos separados
        #{'access_token': 'oauth_token_secret=2f49f8eef6bc4f90729c9cc91708bc431e16b59012be018fc60d46994bd31&oauth_token=79e6d2d319ec8f12b8e6789453d62d300e271be0922779f8723301d0612f7'}

        data
