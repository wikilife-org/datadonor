# coding=utf-8

from social.util.social_service_locator import SocialServiceLocator
from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.aggregated_data import complete_twitter_social_info
from utils.date_util import get_days_twitter

def twitter_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    
    if backend.name == "twitter":
        data = kwargs.get('response')
        dd_user_id = social_user.user.id
        twitter_id = data["id"]
        twitter_service = SocialServiceLocator.get_instane().build_service_by_name("twitter")
        twitter_service.pull_user_info(dd_user_id, {"access_token": data["access_token"]}, twitter_id)
        
        """twitter_id = data["id"]
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
        day_list = get_days_twitter(7)
        
        twitter_tweets_count_last_seven_days = 0
        twitter_retweets_count_last_seven_days = 0
        
        for tweet in timeline:
            tweet_date = "{0} {1}".format(tweet["created_at"][:10], tweet["created_at"][26:])
            if tweet_date in day_list:
                if not "RT @" in tweet["text"]:
                    twitter_tweets_count_last_seven_days = twitter_tweets_count_last_seven_days + 1
                else:
                    twitter_retweets_count_last_seven_days = twitter_retweets_count_last_seven_days + 1
        
        complete_twitter_social_info(social_user.user, int(followers), twitter_tweets_count_last_seven_days, twitter_retweets_count_last_seven_days)
        social_user.extra_data.update(result)
        social_user.save()
          
        return result

def get_user_timeline(backend, access_token):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?exclude_replies=false&include_rts=true&trim_user=true"
    request = build_consumer_oauth_request(backend,access_token, url)
    response = '\n'.join(dsa_urlopen(request.to_url()).readlines())
    response = simplejson.loads(response)
    return response
"""