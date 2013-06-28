"""
{
    'username': u'joaquin',
    'uid': 306340940,
    'twitter': True,
    'is_new': False,
    'auth': <social_auth.backends.twitter.TwitterAuthobjectat0x10e9d7210>,
    'response': {
        u'follow_request_sent': False,
        u'profile_use_background_image': True,
        u'id': 306340940,
        u'verified': False,
        u'entities': {
            u'description': {
                u'urls': [
                    
                ]
            }
        },
        u'profile_image_url_https': u'https: //twimg0-a.akamaihd.net/profile_images/3736951804/72086fe4d25fd6887ba582a39c5da365_normal.png',
        u'profile_sidebar_fill_color': u'C0DFEC',
        u'is_translator': False,
        u'profile_text_color': u'333333',
        u'followers_count': 18,
        u'profile_sidebar_border_color': u'a8c7f7',
        u'id_str': u'306340940',
        u'default_profile_image': False,
        u'location': u'-34.677293,
        -58.633723',
        u'status': {
            u'favorited': False,
            u'in_reply_to_user_id': None,
            u'contributors': None,
            u'truncated': False,
            u'text': u'Cl\xednicadeLosArcosdesdeelbalc\xf3n;miracomobrillaesaluna!http: //t.co/ydmrQTVVzI',
            u'created_at': u'TueJun2501: 16: 13+00002013',
            u'possibly_sensitive_editable': True,
            u'in_reply_to_status_id_str': None,
            u'coordinates': None,
            u'id': 349335185613008896,
            u'entities': {
                u'user_mentions': [
                    
                ],
                u'hashtags': [
                    
                ],
                u'urls': [
                    {
                        u'url': u'http: //t.co/ydmrQTVVzI',
                        u'indices': [
                            65,
                            87
                        ],
                        u'expanded_url': u'http: //instagram.com/p/a9o7CKsFUz/',
                        u'display_url': u'instagram.com/p/a9o7CKsFUz/'
                    }
                ]
            },
            u'in_reply_to_status_id': None,
            u'in_reply_to_screen_name': None,
            u'id_str': u'349335185613008896',
            u'retweeted': False,
            u'place': None,
            u'retweet_count': 0,
            u'geo': None,
            u'in_reply_to_user_id_str': None,
            u'possibly_sensitive': False,
            u'source': u'<ahref="http://instagram.com"rel="nofollow">Instagram</a>'
        },
        u'utc_offset': -10800,
        u'statuses_count': 163,
        u'description': u'LeadSoftwareDeveloper@wikiLifeOrgFoundation.',
        u'friends_count': 52,
        u'profile_background_image_url_https': u'https: //twimg0-a.akamaihd.net/images/themes/theme15/bg.png',
        u'profile_link_color': u'0084B4',
        u'profile_image_url': u'http: //a0.twimg.com/profile_images/3736951804/72086fe4d25fd6887ba582a39c5da365_normal.png',
        u'notifications': False,
        u'geo_enabled': True,
        u'profile_background_color': u'022330',
        u'profile_background_image_url': u'http: //a0.twimg.com/images/themes/theme15/bg.png',
        u'screen_name': u'joa_q',
        u'lang': u'es',
        u'profile_background_tile': False,
        u'favourites_count': 32,
        u'name': u'JoaQ.',
        u'url': None,
        u'created_at': u'FriMay2718: 16: 14+00002011',
        u'contributors_enabled': False,
        u'time_zone': u'BuenosAires',
        'access_token': 'oauth_token_secret=olEIggDcb2td8KIrZ8UTqJkeXgnxcvRTyTTT6eEyk&oauth_token=306340940-3l7Z8yszj6XesGdPFHTG3uLhy3acr9GrTmtnFbbH',
        u'protected': False,
        u'default_profile': False,
        u'following': False,
        u'listed_count': 0
    },
    'new_association': False,
    'user': <User: joaquin>,
    'social_user': <UserSocialAuth: joaquin-Twitter>,
    'details': {
        'username': u'joa_q',
        'fullname': u'JoaQ.',
        'last_name': u'Q.',
        'email': '',
        'first_name': u'Joa'
    },
    'pipeline_index': 11,
    'backend': <social_auth.backends.twitter.TwitterBackendobjectat0x10e9cfa90>
}"""

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request


def twitter_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "twitter":
        data = kwargs.get('response')
        twitter_id = data["id"]
        time_zone = data["time_zone"]
        profile_img = data["profile_image_url_https"]
        follows = data["friends_count"]
        followers = data["followers_count"]
        language = data["lang"]
        geo_location = data["location"]
        tweets_count = data["statuses_count"]
        active_from = data["created_at"]
        fullname = data["name"]
        screen_name = data["screen_name"]
        access_token = data["access_token"]
        result["twitter_id"] = twitter_id
        result["time_zone"] = time_zone
        result["profile_img"] = profile_img
        result["follows"] = follows
        result["followers"] = followers
        result["language"] = language
        result["geo_location"] = geo_location
        result["tweets_count"] = tweets_count
        result["active_from"] = active_from
        result["fullname"] = fullname
        result["screen_name"] = screen_name
        result["access_token"] = access_token
        
        timeline = get_user_timeline(backend, access_token)
        result["timeline"] = timeline
        social_user.extra_data.update(result)
        social_user.save()
          
        return result

def get_user_timeline(backend, access_token):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    request = build_consumer_oauth_request(backend,access_token, url)
    print request.to_url()
    response = '\n'.join(dsa_urlopen(request.to_url()).readlines())
    response = simplejson.loads(response)
    return response
