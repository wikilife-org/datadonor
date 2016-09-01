
from social_auth.models import UserSocialAuth
from social_auth.backends import get_backend
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, date

from uuid import uuid4
import boto
import requests

from social_auth.utils import setting, module_member

import logging
from os import path
from api.models import *

logger = logging.getLogger('datadonors')

file_log_handler = logging.FileHandler(path.join(path.dirname(__file__),'../logs/rest.log'))
logger.addHandler(file_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)


slugify = module_member(setting('SOCIAL_AUTH_SLUGIFY_FUNCTION',
                                'django.template.defaultfilters.slugify'))


from social.util.social_service_locator import SocialServiceLocator
from api.models import Log, Data, TextData



def process_stats(user_id, from_date, to_date):
    result = {}
    #process the logs and data tables using the user_id and date.
    #agreggate according to the user logs and data.
    logs = Log.objects.filter(user__id=user_id, execute_time__gte=from_date, execute_time__lte=to_date)
    
    #agrupar los logs por el nombre, luego agregar los values agrupados por unidad.
    for log in logs:
        print log
    #usar python?
    
    #define the same format for all cases
    

def user_registration(data):
    
    if "facebook" in data.keys():
        return do_facebook_registration(data)
 
    elif "twitter" in data.keys():
        return do_twitter_registration(data)
        
    

def do_twitter_registration(data):
    uid = data["twitter"]["id"]
    backend = get_backend("twitter")
    social_user = UserSocialAuth.get_social_auth(backend.name, uid)
    
    if social_user:
        social_user.extra_data = data["twitter"]
        social_user.save()
    
    else:
        
        user = UserSocialAuth.create_user(username=get_username(), email="")
        Profile.objects.create(user=user)
        social_user = UserSocialAuth.objects.create(user=user, provider="twitter", uid=uid, extra_data=data["twitter"])
        
    dd_user_id = social_user.user.id
    twitter_service = SocialServiceLocator.get_instane().build_service_by_name("twitter")
    twitter_service.pull_user_info(dd_user_id, {"access_token": data["twitter"]["access_token"], "twitter_id": uid})

    return dd_user_id 
   
def do_facebook_registration(data):
    print data
    uid = data["facebook"]["id"]
    #backend = get_backend("facebook")
    social_user = UserSocialAuth.get_social_auth("facebook", uid)
    
    if social_user:
        social_user.extra_data = data["facebook"]
        social_user.save()
    
    else:
        user = UserSocialAuth.create_user(username=get_username(), email="")
        Profile.objects.get_or_create(user=user)
        social_user = UserSocialAuth.objects.create(user=user, provider="facebook", uid=uid, extra_data=data["facebook"])
        
    dd_user_id = social_user.user.id
    facebook_service = SocialServiceLocator.get_instane().build_service_by_name("facebook")
    facebook_service.pull_user_info(dd_user_id, {"access_token": data["facebook"]["access_token"]})

    return dd_user_id 
   
def get_username(
                 user_exists=UserSocialAuth.simple_user_exists,
                 ):
    """Return an username for new user. Return current user username
    if user was given.
    """

    uuid_length = setting('SOCIAL_AUTH_UUID_LENGTH', 16)
    do_slugify = setting('SOCIAL_AUTH_SLUGIFY_USERNAMES', False)

    username = uuid4().get_hex()

    max_length = UserSocialAuth.username_max_length()
    short_username = username[:max_length - uuid_length]
    final_username = UserSocialAuth.clean_username(username[:max_length])
    if do_slugify:
        final_username = slugify(final_username)

    # Generate a unique username for current user using username
    # as base but adding a unique hash at the end. Original
    # username is cut to avoid any field max_length.
    while user_exists(username=final_username):
        username = short_username + uuid4().get_hex()[:uuid_length]
        username = username[:max_length]
        final_username = UserSocialAuth.clean_username(username)
        if do_slugify:
            final_username = slugify(final_username)
    print final_username
    return final_username


def process_log(post_content, user):
    location, weather = process_location(post_content.get("lat", None), post_content.get("lon", None))

    text = post_content["text"]
    
    processed_text = process_text(text)
    category = processed_text["category"]
    wiki_node_id = processed_text["wiki_node_id"]
    wiki_node_name = processed_text["wiki_node_name"]
    source = post_content.get("source", None)
    
    time_obj = post_content["time_obj"] #Format?
    
    
    log = Log.objects.create(user=user, location=location, 
                             weather=weather, 
                             category=category, text=text, 
                             wiki_node_name=wiki_node_name, 
                             wiki_node_id=wiki_node_id,
                             source=source,
                             execute_time = time_obj )

    for d in processed_text["data"]:
        unit = d["unit"]
        value = int(d["value"])
        slug_unit = d["slug_unit"]
        wiki_node_id_text = d["wiki_node_id"]
        wiki_node_name_text = d["wiki_node_name"]
        TextData.objects.create(log=log,unit=unit, slug_unit=slug_unit ,value=value, wiki_node_id=wiki_node_id_text, wiki_node_name=wiki_node_name_text  )
        
      
    data = process_data(post_content)
    for d in data:
        unit_data = d["unit"]
        value_data = int(d["value"])
        slug_unit_data = d["slug_unit"]
        wiki_node_id_data = d["wiki_node_id"]
        wiki_node_name_data = d["wiki_node_name"]
        Data.objects.create(log=log, unit=unit_data, value=value_data, slug_unit=slug_unit_data, wiki_node_id= wiki_node_id_data, wiki_node_name=wiki_node_name_data)

    return log.id

from boto.s3.key import Key
import base64

def upload_image(data, log_id):
    logger.error("Pre S3 upload")
    key = "AKIA___I42N5MA___H34RI____JERA".replace("_", "")
    secret = "766i___UxRQZoq5h___iVTHQLGUYVzxM____rr6H82___5k4khJga".replace("_", "")
    conn = boto.connect_s3(key, secret)
    logger.error("1")
    bucket = conn.get_bucket("datadonors-app")
    logger.error("2")
    k = Key(bucket)
    logger.error("3")
    k.key = "%s.jpg"%(log_id)
    logger.error("4")
    k.set_metadata('Content-Type', 'image/jpeg')
    logger.error("5")
    k.set_contents_from_string(base64.b64decode(data))
    logger.error("6")
    k.set_acl('public-read')
    logger.error("7")
    url = k.generate_url(expires_in=0, query_auth=False, force_http=True)
    logger.error("After s3 Upload")
    logger.error(url)
    return url

def process_text(text):
    #NL or regex funcionts
    #Go to Wikilife, check if node exists, get metrics
    search_exact_url = "http://api.wikilife.org/4/meta/exact/search/?name=%s"%text
    search_url = "http://api.wikilife.org/4/meta/search/?name=%s"%text
    result = {}
    items =  requests.get(search_exact_url).json()["items"]
    category = None
    wiki_node_id = None
    wiki_node_name = None
    
    for item in items:
        if "is" in item:
            if len(item["is"]) >0 :
                category = item["is"][0]["name"]
                wiki_node_id = item["id"]
                wiki_node_name = item["name"]
                break
            
    if category == None:
        items =  requests.get(search_url).json()["items"]
        for item in items:
            if "is" in item:
                if len(item["is"]) >0 :
                    category = item["is"][0]["name"]
                    break
        
    result["category"] = category 
    result["wiki_node_id"] = wiki_node_id
    result["wiki_node_name"] = wiki_node_name
    
    #Metrics from wikiNode
    result["data"] = []
    
    return result

from api.models import Data

def process_data(data):
    prop1_name = data.get("prop1_name", None)
    prop1_value = data.get("prop1_value", None)
    prop2_name = data.get("prop2_name", None)
    prop2_value = data.get("prop2_value", None)
    result = []
    
    if prop1_name and prop1_value:
        slug_unit = slugify(prop1_name)
        d = {}
        d["unit"] = prop1_name
        d["value"] = int(prop1_value)
        d["slug_unit"] = slug_unit
        d["wiki_node_id"] = None
        d["wiki_node_name"] = None
        result.append(d)
    
    if prop2_name and prop2_value:
        slug_unit = slugify(prop2_name)
        d = {}
        d["unit"] = prop2_name
        d["value"] = int(prop2_value)
        d["slug_unit"] = slug_unit
        d["wiki_node_id"] = None
        d["wiki_node_name"] = None
        result.append(d)
    
    return result
    

def process_location(lat=None, lon=None):
    location = None
    weather = None
    
    if lat and lon:
        lat = "%s"%round(float(lat),2)
        lon = "%s"%round(float(lon),2)
        location, created = Location.objects.get_or_create(lat=lat, lon=lon)
        weather, created = WeatherByDay.objects.get_or_create(location=location, date=date.today())
        if created:
            url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&APPID=7341d32aee1f6e63e10ce24f3f5ecbcc&units=metric".format(lat, lon)
            print url
            try:
                result = requests.get(url).json()
                print result
                name = result.get("name", None)
                if "coord" in result:
                    lat = result["coord"]["lat"]
                    lon = result["coord"]["lon"]
                    
                
                country = None
                if "sys" in result:
                    country = result["sys"].get("country", None)
                    location.country = country
                location.region = name
                location.save()
                weather.temp_f= result["weather"][0]
                weather.temp_c = result["main"]["temp"]
                weather.weather= result["weather"][0]["main"]
                weather.icon = result["weather"][0]["icon"]
                weather.save()
            except:
                weather.delete()
                location = None
                weather = None
            
    return location, weather


def get_user_timeline(user_id, from_id=None, limit=10, sort="desc"):
    result = []
    print from_id
    if sort == "desc":
        q_sort = "-execute_time"
    else:
        q_sort = "execute_time"
    try:
        qs = Log.objects.filter(user__id=int(user_id)).order_by(q_sort)
        if from_id:
            qs = qs.filter(id__lte=int(from_id))
        result = [a.to_dict() for a in qs[:limit]]
    except:
        pass
    return result


def delete_user_log(user, log_id):
    log = Log.objects.get(id=int(log_id))
    log.delete()
