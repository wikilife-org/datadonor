
from social_auth.models import UserSocialAuth
from social_auth.backends import get_backend
from users.models import Profile
from django.contrib.auth.models import User
from uuid import uuid4
import boto
from social_auth.utils import setting, module_member


slugify = module_member(setting('SOCIAL_AUTH_SLUGIFY_FUNCTION',
                                'django.template.defaultfilters.slugify'))


from social.util.social_service_locator import SocialServiceLocator
from rest.models import Log, Data, TextData


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
    uid = data["facebook"]["id"]
    backend = get_backend("facebook")
    social_user = UserSocialAuth.get_social_auth(backend.name, uid)
    
    if social_user:
        social_user.extra_data = data["facebook"]
        social_user.save()
    
    else:
        user = UserSocialAuth.create_user(username=get_username(), email="")
        Profile.objects.create(user=user)
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
    return username


def process_log(post_content, user):
    location, weather = process_location(post_content["location"])

    text = post_content["text"]
    
    processed_text = process_text(text)
    category = processed_text["category"]
    wiki_node_id = processed_text["wiki_node_id"]
    wiki_node_name = processed_text["wiki_node_name"]
    
    time = post_content["time"] #Format?
    
    
    log = Log.objects.create(user=user, location=location, weather=weather, category=category, text=text, wiki_node_name=wiki_node_name, wiki_node_id=wiki_node_id )

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

def upload_image(data, log_id):
    conn = boto.connect_s3("AWS_ACCESS_KEYXXX", "AWS_SECRET_KEYXXX")
    bucket = conn.get_bucket("datadonors_user_images")
    k = boto.Key(bucket)
    k.key = "%s"%(log_id)
    k.set_metadata('Content-Type', 'image/jpeg')
    k.set_contents_from_file(data)

def process_text(text):
    #NL or regex funcionts
    #Go to Wikilife, check if node exists, get metrics
    return None

def process_data(data):
    prop1_name = data.get("prop1_name", None)
    prop1_value = data.get("prop1_value", None)
    prop2_name = data.get("prop2_name", None)
    prop2_value = data.get("prop2_value", None)
    
    result = []
    return result
    

def process_location(data):
    return None, None
