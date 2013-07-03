
"""
{
    'username': u'tests',
    'uid': u'100006128858058',
    'is_new': False,
    'auth': <social_auth.backends.facebook.FacebookAuthobjectat0x10d886e50>,
    'new_association': False,
    'facebook': True,
    'user': <django.utils.functional.SimpleLazyObjectobjectat0x10d886c10>,
    'social_user': <UserSocialAuth: tests-Facebook>,
    'response': {
        u'username': u'wikilife.development',
        u'first_name': u'Wikilife',
        u'last_name': u'Development',
        u'verified': True,
        u'name': u'WikilifeDevelopment',
        u'locale': u'es_LA',
        u'gender': u'male',
        'expires': '5182651',
        u'email': u'jquintas@wikilife.org',
        'access_token': 'CAACYMya0cUsBAJ1elZAxMZA0095cyQWrtjeF77Gg3ZBFu3azIiKWb6MSAGTvii5vq8XgqcIVLIrwR5okoRMfSOyroIINCEkkvz8clYpZB1lynzLOyjY7ZCB6nCuT1BEBV92gkJBWV7VXRXvWh8BilCDcvnIQcIU4ZD',
        u'birthday': u'10/10/1970',
        u'link': u'http: //www.facebook.com/wikilife.development',
        u'timezone': -3,
        u'updated_time': u'2013-06-14T15: 35: 51+0000',
        u'id': u'100006128858058'
    },
    'backend': <social_auth.backends.facebook.FacebookBackendobjectat0x10d897650>,
    'pipeline_index': 11,
    'details': {
        'username': u'wikilife.development',
        'fullname': u'WikilifeDevelopment',
        'last_name': u'Development',
        'email': u'jquintas@wikilife.org',
        'first_name': u'Wikilife'
    }
}
"""
import urllib2

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.facebook import GraphAPI

def facebook_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "facebook":
        data = kwargs.get('response')
        
        facebook_id = data["id"]
        time_zone = data["timezone"]
        birthday = data["birthday"]
        email = data["email"]
        user_name = data["username"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        locale = data["locale"]
        gender = data["gender"]
        access_token = data["access_token"]
        hometown = data.get("hometown", {})
        work = data.get("work", [])
        education  = data.get("education", [])
        languages = data.get("languages", [])
        
        profile_img = load_profile_pic(facebook_id)
        graph = GraphAPI(access_token)
        total_friend = graph.fql("SELECT friend_count FROM user WHERE uid = me()")[0]["friend_count"]
        albums = graph.get_connections("me", "albums")
        total_photos = 0
        for photos in albums:
            total_photos += photos["count"]
        
        total_likes = graph.fql("SELECT user_id, object_id, post_id FROM like WHERE user_id=me()")
        #print graph.get_object("me")
        
        result["facebook_id"] = facebook_id
        result["time_zone"] = time_zone
        result["birthday"] = birthday
        result["email"] = email
        result["user_name"] = user_name
        result["first_name"] = first_name
        result["last_name"] = last_name
        result["locale"] = locale
        result["gender"] = gender
        result["access_token"] = access_token
        result["hometown"] = hometown
        result["work"] = work
        result["education"] = education
        result["languages"] = languages
        result["profile_img"] = profile_img
        result["total_friend"] = total_friend
        result["total_photos"] = total_photos
        result["total_likes"] = total_likes
        
        social_user.extra_data.update(result)
        social_user.save()
          
        return result
    

def load_profile_pic(faceboof_id):

    url = "http://graph.facebook.com/%s/picture?width=200&height=200&redirect=false" % faceboof_id
    data = simplejson.loads(urllib2.urlopen(url).read())['data']
    return data["url"]



        