# coding=utf-8

from social.models import Profile, SocialUserAggregatedData
from wikilife.client.logs import Logs
from wikilife.client.user import User
from wikilife_utils.logs.log_creator import LogCreator


class WikilifeConnectorException(Exception):
    pass


class WikilifeConnector(object):

    _user_client = None
    _log_client = None
    _log_creator = None

    """
    def __init__(self, user_client, log_client, log_creator):
        self._user_client = user_client
        self._log_client = log_client
        self._log_creator = log_creator
    """
    def __init__(self, logger, wikilife_settings):
        self._user_client = User(logger, wikilife_settings)
        self._log_client = Logs(logger, wikilife_settings)
        self._log_creator = LogCreator()

    def push(self):
        """
        send new user accounts
        send new social user data

        read from datadonor
        write to wikilife
        """
        self._push_users()
        self._push_logs()

    def _push_users(self):
        for profile in Profile.objects.filter(wikilife_token=None):
            user_name = self._create_user_name(profile.account_id)
            pin = "0000"
            gender = profile.gender
            birthdate = profile.date_of_birth
            height = None
            weight = None
            device_id = None
            timezone = None
            city = None
            region = None
            country = None
            success = self._user_client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)

            if not success:
                raise WikilifeConnectorException("Wikilife account creation failed for Datadonor profile.account_id: %s" %profile.account_id)

            token = self._user_client.login(user_name, pin)
            profile.wikilife_token = token
            profile.save()
    
    def _create_user_name(self, unique_id):
        base_user_name = "datadonor_"
        user_name = "%s%s" %(base_user_name, unique_id)

        i = 1
        while not self._user_client.check_name(user_name):
            user_name = "%s%s_$s" %(base_user_name, unique_id, i)
            i += 1

        return user_name

    def _push_logs(self):
        prev_user = None

        for item in SocialUserAggregatedData.objects.filter(wikilife_ids=None).order_by('user'):
            if prev_user != item.user:
                oauth_token = Profile.objects.get(user=item.user).wikilife_token

            logs = self._create_logs(item)
            inserted_ids = self._log_client.add_logs(oauth_token, logs)
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
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.facebook_friend_count))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.facebook_post_count_last_seven_days))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.facebook_likes_count_last_seven_days))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.twitter_followers_count))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.twitter_tweets_count_last_seven_days))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.twitter_retweets_count_last_seven_days))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.gmail_contacts_count))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.linkedin_connections_count))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.foursquare_friends_count))

        log_social = self._log_creator.create_log(user_id, start, end, text, source, nodes)

        text = "Datadonor profile"
        nodes = []
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.education_level))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.education_degree))
        nodes.append(self._log_creator.create_log_node(node_id=0, metric_id=0, value=s.work_experience_years))

        log_profile = self._log_creator.create_log(user_id, start, end, text, source, nodes)

        return [log_social, log_profile]

    def pull(self):
        """.
        get global social data

        read from wikilife
        write to datadonor
        """
        self._pull_education()
        self._pull_social()

    def _pull_education(self):
        
        