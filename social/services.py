from social_auth.models import *

def global_social_reach():
    return {"facebook":{"count": 20, "percentage":20}, "twitter":{"count": 20, "percentage":10},
                "gmail":{"count": 20, "percentage":10}, "foursquare":{"count": 20, "percentage":40},
                "linkedin":{"count": 20, "percentage":20}}

def global_social_sharing():
    return {"facebook":{"posts":134, "likes":44}, "twitter":{"tweets":99, "retweets":12}}
