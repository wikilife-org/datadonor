
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
import math
from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.facebook import GraphAPI, GraphAPIError
from datetime import date, timedelta, datetime
from utils.aggregated_data import complete_facebook_info, complete_profile

def facebook_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    
    if backend.name == "facebook":
        
        data = kwargs.get('response')
        
        facebook_id = data.get("id", "")
        time_zone = data.get("timezone", "")
        birthday = data.get("birthday", "")
        email = data.get("email", "")
        user_name = data.get("username", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        locale = data.get("locale", "")
        gender = data.get("gender", "")
        access_token = data.get("access_token", "")
        hometown = data.get("hometown", {})
        work = data.get("work", [])
        education  = data.get("education", [])
        languages = data.get("languages", [])
        
        #profile_img = load_profile_pic(facebook_id)
        
        graph = GraphAPI(access_token)

        total_friend = graph.fql("SELECT friend_count FROM user WHERE uid = me()")[0]["friend_count"]
        
        """        
        albums = graph.get_connections("me", "albums")

        total_photos = 0
        for photos in albums["data"]:
            total_photos += photos["count"]

        """
        today = date.today()

        
        total_likes_query = "SELECT object_id FROM like WHERE user_id=me() limit 5000"
        total_likes = graph.fql(total_likes_query)
        count_likes = len(total_likes)
        index = count_likes - 1
        avg_likes = 0
        f_object = None
        
        while f_object is None and index >= 0:
            try:
                f_object = graph.get_object(total_likes[index]["object_id"])
            except GraphAPIError:
                index = index - 1
        
        if f_object:
            try:
                update_date = datetime.strptime(f_object["created_time"][:10], "%Y-%m-%d").date()
            except:
                update_date = datetime.strptime(f_object["updated_time"][:10], "%Y-%m-%d").date()
            weeks = ((today - update_date).days or 7) / 7
            avg_likes = int(math.ceil((index + 1) / weeks))
        
        
        posts = graph.request("me/posts", {"limit":1000})
        index = len(posts["data"]) - 1
        initial_date = datetime.strptime(posts["data"][index]["created_time"][:10], "%Y-%m-%d").date()
        weeks = (today - initial_date).days / 7
        avg_posts = int(math.ceil((index + 1) / weeks))
        
        complete_facebook_info(social_user.user, total_friend, avg_posts, avg_likes)
        
        if gender:
            if gender =="male":
                gender = "m"
            elif gender == "female":
                gender = "f"
        
        birthdate = None
        if birthday:
            birthdate = datetime.strptime(birthday, "%m/%d/%Y").date()
        complete_profile(social_user.user, email, birthdate, gender)
        
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
        #result["profile_img"] = profile_img
        result["total_friend"] = total_friend
        #result["total_photos"] = total_photos
        result["avg_likes_weekly"] = avg_likes
        result["avg_post_weekly"] = avg_posts
        
        social_user.extra_data.update(result)
        social_user.save()
          
        return result
    

def load_profile_pic(faceboof_id):

    url = "http://graph.facebook.com/%s/picture?width=200&height=200&redirect=false" % faceboof_id
    data = simplejson.loads(urllib2.urlopen(url).read())['data']
    return data["url"]



        