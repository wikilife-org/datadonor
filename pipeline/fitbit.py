
from physical.util.physical_service_locator import PhysicalServiceLocator


def fitbit_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "fitbit":
        data = kwargs.get('response')
        dd_user_id = request.user.id
        fitbit_service = PhysicalServiceLocator.get_instane().get_service_by_name("fitbit")
        fitbit_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]})

    
def get_user_profile(backend, access_token, fitbit_id):
    url = "http://api.fitbit.com/1/user/%s/profile.json" %fitbit_id
    request = build_consumer_oauth_request(backend.name,access_token, url)
    response = requests.request("GET", url, headers=request.to_header())
    return response.json()

def get_user_activity(backend, access_token, fitbit_id):
    day_list = get_days_list(7)
    result = {}
    for day in day_list:
        day_formatted = day.strftime("%Y-%m-%d")
        url = "http://api.fitbit.com/1/user/%s/activities/date/%s.json" %(fitbit_id, day_formatted)
        request = build_consumer_oauth_request(backend,access_token, url)
        response = requests.request("GET", url, headers=request.to_header())
        result[day_formatted] = response.json()
    
    return result

def get_user_food(backend, access_token, fitbit_id):
    day_list = get_days_list(7)
    result = {}
    for day in day_list:
        day_formatted = day.strftime("%Y-%m-%d")
        url = "http://api.fitbit.com/1/user/%s/foods/log/date/%s.json" %(fitbit_id, day_formatted)
        request = build_consumer_oauth_request(backend,access_token, url)
        response = requests.request("GET", url, headers=request.to_header())
        result[day_formatted] = response.json()
    
    return result
    