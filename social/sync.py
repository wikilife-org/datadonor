# coding=utf-8

from social.models import Profile, SocialUserAggregatedData, \
    GlobalEducationDistribution, GlobalWorkExperinceDistribution, \
    SocialGlobalAggregatedData
from wikilife.base_sync import BaseSync
from wikilife_utils.logs.log_creator import LogCreator


class SocialSync(BaseSync):

    _logs_client = None
    _stats_client = None

    def __init__(self, logs_client, stats_client):
        self._logs_client = logs_client
        self._stats_client = stats_client

    def sync(self):
        """
        Pull from sources
        Push to Wikilife
        """
        self._pull()
        self._push()

    def _push(self):
        """
        send new social user data
        read from datadonor
        write to wikilife
        """
        self._push_logs()

    def _push_logs(self):
        prev_user = None

        #TODO 
        for item in SocialUserAggregatedData.objects.filter(wikilife_ids=None).order_by('user'):
            if prev_user != item.user:
                oauth_token = Profile.objects.get(user=item.user).wikilife_token

            logs = self._create_logs(item)
            inserted_ids = self._logs_client.add_logs(oauth_token, logs)
            item.wikilife_ids = ",".join(inserted_ids)
            item.save()

    def _create_logs(self, social_item):
        s = social_item

        user_id = 0
        start = s.create_time
        end = s.create_time
        source = "Datadonor WikilifeConnector"

        text = "Datadonor social"
        nodes = []
        nodes.append(LogCreator.create_log_node(node_id=216818, metric_id=216810, value=s.facebook_friend_count))
        nodes.append(LogCreator.create_log_node(node_id=216818, metric_id=216807, value=s.facebook_post_count_last_seven_days))
        nodes.append(LogCreator.create_log_node(node_id=216818, metric_id=216805, value=s.facebook_likes_count_last_seven_days))
        nodes.append(LogCreator.create_log_node(node_id=216819, metric_id=216798, value=s.twitter_followers_count))
        nodes.append(LogCreator.create_log_node(node_id=216819, metric_id=216811, value=s.twitter_tweets_count_last_seven_days))
        nodes.append(LogCreator.create_log_node(node_id=216819, metric_id=216802, value=s.twitter_retweets_count_last_seven_days))
        nodes.append(LogCreator.create_log_node(node_id=216820, metric_id=216801, value=s.gmail_contacts_count))
        nodes.append(LogCreator.create_log_node(node_id=216821, metric_id=216799, value=s.foursquare_friends_count))
        nodes.append(LogCreator.create_log_node(node_id=3176, metric_id=3171, value=s.linkedin_connections_count))

        log_social = LogCreator.create_log(user_id, start, end, text, source, nodes)

        text = "Datadonor profile"
        nodes = []
        nodes.append(LogCreator.create_log_node(node_id=2, metric_id=216809, value=s.education_degree))
        nodes.append(LogCreator.create_log_node(node_id=216815, metric_id=216806, value=s.work_experience_years))

        log_profile = LogCreator.create_log(user_id, start, end, text, source, nodes)

        return [log_social, log_profile]

    def _pull(self):
        """.
        get global social data

        read from wikilife
        write to datadonor
        """
        education_item = self._pull_education()
        work_item = self._pull_work()
        self._pull_social(education_item, work_item)

    _education_match_options = {
        "elementary": "Elementary School",
        "high_school": "High School",
        "junior_college": "Junior College",
        "tech": "Technical Institute",
        "university": "University",
        "master": "Master's Degree",
        "phd": "Ph.D"
    }

    def _pull_education(self):
        m = self._education_match_options
        r = self._stats_client.get_global_education_stats()
        s = r["data"]

        item = GlobalEducationDistribution(
            elementary=s[m["elementary"]]["percent"], 
            high_school=s[m["high_school"]]["percent"], 
            junior_collage=s[m["junior_college"]]["percent"], 
            tech=s[m["tech"]]["percent"], 
            university=s[m["university"]]["percent"], 
            master=s[m["master"]]["percent"], 
            phd=s[m["phd"]]["percent"] 
        )
        return item

    def _pull_work(self):
        r = self._stats_client.get_global_work_stats()
        s = r["data"]["buckets"]
        VALUE_KEY = "experienceAvg"
        
        item = GlobalWorkExperinceDistribution(
            range_15_25=s[0][VALUE_KEY], 
            range_25_35=s[1][VALUE_KEY], 
            range_36_45=s[2][VALUE_KEY], 
            range_46_55=s[3][VALUE_KEY], 
            range_56_65=s[4][VALUE_KEY]
        )
        return item 

    _social_match_lvs = {
        "avg_facebook_friend_count": "Facebook.Friends", 
        "facebook_post_weekly_avg": "Facebook.Posts", 
        "facebook_likes_weekly_avg": "Facebook.Likes given",
        "avg_twitter_followers_count": "Twitter.Followers",
        "avg_twitter_tweets_count_last_seven_days": "Twitter.Tweets", 
        "avg_twitter_retweets_count_last_seven_days": "Twitter.Retweets",
        "gplus_contacts_count": "Gmail.Contacts",
        "avg_linkedin_connections_count": "LinkedIn.Connections",
        "avg_foursquare_connections_count": "Foursquare.Friends"
    }

    def _pull_social(self, education_item, work_item):
        m = self._social_match_lvs
        r = self._stats_client.get_global_social_stats()
        s = r["data"]

        education_item.save()
        work_item.save()

        item = SocialGlobalAggregatedData(
            avg_facebook_friend_count=s[m["avg_facebook_friend_count"]]["avg"], 
            facebook_post_weekly_avg=s[m["facebook_post_weekly_avg"]]["avg"], 
            facebook_likes_weekly_avg=s[m["facebook_likes_weekly_avg"]]["avg"], 
            avg_twitter_followers_count=s[m["avg_twitter_followers_count"]]["avg"],
            avg_twitter_tweets_count_last_seven_days=s[m["avg_twitter_tweets_count_last_seven_days"]]["avg"],
            avg_twitter_retweets_count_last_seven_days=s[m["avg_twitter_retweets_count_last_seven_days"]]["avg"], 
            gplus_contacts_count=s[m["gplus_contacts_count"]]["avg"],
            avg_linkedin_connections_count=s[m["avg_linkedin_connections_count"]]["avg"],
            avg_foursquare_connections_count=s[m["avg_foursquare_connections_count"]]["avg"],
            education=education_item,
            work_experience=work_item 
        )
        item.save()