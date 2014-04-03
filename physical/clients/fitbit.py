# -*- coding: utf-8 -*-
import oauth2 as oauth
import requests
import json
import datetime
import urllib

from requests_oauthlib import OAuth1Session

def curry(_curried_func, *args, **kwargs):
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*(args+moreargs), **dict(kwargs, **morekwargs))
    return _curried

class Fitbit(object):
    US = 'en_US'
    METRIC = 'en_UK'

    API_ENDPOINT = "https://api.fitbit.com"
    API_VERSION = 1
    WEEK_DAYS = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']

    _resource_list = [
        'body',
        'activities',
        'foods',
        'water',
        'sleep',
        'heart',
        'bp',
        'glucose',
    ]

    _qualifiers = [
        'recent',
        'favorite',
        'frequent',
    ]

    def __init__(self, consumer_key, consumer_secret, system=US, **kwargs):
        self.client = FitbitOauthClient(consumer_key, consumer_secret, **kwargs)
        self.SYSTEM = system

        # All of these use the same patterns, define the method for accessing
        # creating and deleting records once, and use curry to make individual
        # Methods for each
        for resource in self._resource_list:
            setattr(self, resource, curry(self._COLLECTION_RESOURCE, resource))

            if resource not in ['body', 'glucose']:
                # Body and Glucose entries are not currently able to be deleted
                setattr(self, 'delete_%s' % resource, curry(
                    self._DELETE_COLLECTION_RESOURCE, resource))

        for qualifier in self._qualifiers:
            setattr(self, '%s_activities' % qualifier, curry(self.activity_stats, qualifier=qualifier))
            setattr(self, '%s_foods' % qualifier, curry(self._food_stats,
                                                        qualifier=qualifier))

    def make_request(self, *args, **kwargs):
        ##@ This should handle data level errors, improper requests, and bad
        # serialization
        headers = kwargs.get('headers', {})
        headers.update({'Accept-Language': self.SYSTEM})
        kwargs['headers'] = headers

        method = kwargs.get('method', 'POST' if 'data' in kwargs else 'GET')
        response = self.client.make_request(*args, **kwargs)

        if response.status_code == 202:
            return True
        if method == 'DELETE':
            if response.status_code == 204:
                return True
            else:
                raise DeleteError(response)
        try:
            rep = json.loads(response.content)
        except ValueError:
            raise BadResponse

        return rep

    def user_profile_get(self, user_id=None):
        """
        Get a user profile. You can get other user's profile information
        by passing user_id, or you can get the current user's by not passing
        a user_id

        .. note:
            This is not the same format that the GET comes back in, GET requests
            are wrapped in {'user': <dict of user data>}

        https://wiki.fitbit.com/display/API/API-Get-User-Info
        """
        if user_id is None:
            user_id = "-"
        url = "%s/%s/user/%s/profile.json" % (self.API_ENDPOINT,
                                              self.API_VERSION, user_id)
        return self.make_request(url)

    def user_profile_update(self, data):
        """
        Set a user profile. You can set your user profile information by
        passing a dictionary of attributes that will be updated.

        .. note:
            This is not the same format that the GET comes back in, GET requests
            are wrapped in {'user': <dict of user data>}

        https://wiki.fitbit.com/display/API/API-Update-User-Info
        """
        url = "%s/%s/user/-/profile.json" % (self.API_ENDPOINT,
                                              self.API_VERSION)
        return self.make_request(url, data)

    def _COLLECTION_RESOURCE(self, resource, date=None, user_id=None,
                             data=None):
        """
        Retrieving and logging of each type of collection data.

        Arguments:
            resource, defined automatically via curry
            [date] defaults to today
            [user_id] defaults to current logged in user
            [data] optional, include for creating a record, exclude for access

        This implements the following methods::

            body(date=None, user_id=None, data=None)
            activities(date=None, user_id=None, data=None)
            foods(date=None, user_id=None, data=None)
            water(date=None, user_id=None, data=None)
            sleep(date=None, user_id=None, data=None)
            heart(date=None, user_id=None, data=None)
            bp(date=None, user_id=None, data=None)

        * https://wiki.fitbit.com/display/API/Fitbit+Resource+Access+API
        """

        if not date:
            date = datetime.date.today()
        if not user_id:
            user_id = '-'
        if not isinstance(date, basestring):
            date = date.strftime('%Y-%m-%d')

        if not data:
            url = "%s/%s/user/%s/%s/date/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                resource,
                date,
            )
        else:
            data['date'] = date
            url = "%s/%s/user/%s/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                resource,
            )
        return self.make_request(url, data)

    def _DELETE_COLLECTION_RESOURCE(self, resource, log_id):
        """
        deleting each type of collection data

        Arguments:
            resource, defined automatically via curry
            log_id, required, log entry to delete

        This builds the following methods::

            delete_body(log_id)
            delete_activities(log_id)
            delete_foods(log_id)
            delete_water(log_id)
            delete_sleep(log_id)
            delete_heart(log_id)
            delete_bp(log_id)

        """
        url = "%s/%s/user/-/%s/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            resource,
            log_id,
        )
        response = self.make_request(url, method='DELETE')
        return response

    def time_series(self, resource, user_id=None, base_date='today',
                    period=None, end_date=None):
        """
        The time series is a LOT of methods, (documented at url below) so they
        don't get their own method. They all follow the same patterns, and
        return similar formats.

        Taking liberty, this assumes a base_date of today, the current user,
        and a 1d period.

        https://wiki.fitbit.com/display/API/API-Get-Time-Series
        """
        if not user_id:
            user_id = '-'

        if period and end_date:
            raise TypeError("Either end_date or period can be specified, not both")

        if end_date:
            if not isinstance(end_date, basestring):
                end = end_date.strftime('%Y-%m-%d')
            else:
                end = end_date
        else:
            if not period in ['1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']:
                raise ValueError("Period must be one of '1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max'")
            end = period

        if not isinstance(base_date, basestring):
            base_date = base_date.strftime('%Y-%m-%d')

        url = "%s/%s/user/%s/%s/date/%s/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            user_id,
            resource,
            base_date,
            end
        )
        return self.make_request(url)

    def activity_stats(self, user_id=None, qualifier=''):
        """
        * https://wiki.fitbit.com/display/API/API-Get-Activity-Stats
        * https://wiki.fitbit.com/display/API/API-Get-Favorite-Activities
        * https://wiki.fitbit.com/display/API/API-Get-Recent-Activities
        * https://wiki.fitbit.com/display/API/API-Get-Frequent-Activities

        This implements the following methods::

            recent_activities(user_id=None, qualifier='')
            favorite_activities(user_id=None, qualifier='')
            frequent_activities(user_id=None, qualifier='')
        """
        if not user_id:
            user_id = '-'

        if qualifier:
            if qualifier in self._qualifiers:
                qualifier = '/%s' % qualifier
            else:
                raise ValueError("Qualifier must be one of %s"
                    % ', '.join(self._qualifiers))
        else:
            qualifier = ''

        url = "%s/%s/user/%s/activities%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            user_id,
            qualifier,
        )
        return self.make_request(url)

    def _food_stats(self, user_id=None, qualifier=''):
        """
        This builds the convenience methods on initialization::

            recent_foods(user_id=None, qualifier='')
            favorite_foods(user_id=None, qualifier='')
            frequent_foods(user_id=None, qualifier='')

        * https://wiki.fitbit.com/display/API/API-Get-Recent-Foods
        * https://wiki.fitbit.com/display/API/API-Get-Frequent-Foods
        * https://wiki.fitbit.com/display/API/API-Get-Favorite-Foods
        """
        if not user_id:
            user_id = '-'

        url = "%s/%s/user/%s/foods/log/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            user_id,
            qualifier,
        )
        return self.make_request(url)

    def add_favorite_activity(self, activity_id):
        """
        https://wiki.fitbit.com/display/API/API-Add-Favorite-Activity
        """
        url = "%s/%s/user/-/activities/favorite/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            activity_id,
        )
        return self.make_request(url, method='POST')

    def log_activity(self, data):
        """
        https://wiki.fitbit.com/display/API/API-Log-Activity
        """
        url = "%s/%s/user/-/activities.json" % (
            self.API_ENDPOINT,
            self.API_VERSION)
        return self.make_request(url, data = data)

    def delete_favorite_activity(self, activity_id):
        """
        https://wiki.fitbit.com/display/API/API-Delete-Favorite-Activity
        """
        url = "%s/%s/user/-/activities/favorite/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            activity_id,
        )
        return self.make_request(url, method='DELETE')

    def add_favorite_food(self, food_id):
        """
        https://wiki.fitbit.com/display/API/API-Add-Favorite-Food
        """
        url = "%s/%s/user/-/foods/log/favorite/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            food_id,
        )
        return self.make_request(url, method='POST')

    def delete_favorite_food(self, food_id):
        """
        https://wiki.fitbit.com/display/API/API-Delete-Favorite-Food
        """
        url = "%s/%s/user/-/foods/log/favorite/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            food_id,
        )
        return self.make_request(url, method='DELETE')

    def create_food(self, data):
        """
        https://wiki.fitbit.com/display/API/API-Create-Food
        """
        url = "%s/%s/user/-/foods.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url, data=data)

    def get_meals(self):
        """
        https://wiki.fitbit.com/display/API/API-Get-Meals
        """
        url = "%s/%s/user/-/meals.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url)

    def get_devices(self):
        """
        https://wiki.fitbit.com/display/API/API-Get-Devices
        """
        url = "%s/%s/user/-/devices.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url)

    def get_alarms(self, device_id):
        """
        https://wiki.fitbit.com/display/API/API-Devices-Get-Alarms
        """
        url = "%s/%s/user/-/devices/tracker/%s/alarms.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            device_id
        )
        return self.make_request(url)

    def add_alarm(self, device_id, alarm_time, week_days, recurring=False, enabled=True, label=None,
                     snooze_length=None, snooze_count=None, vibe='DEFAULT'):
        """
        https://wiki.fitbit.com/display/API/API-Devices-Add-Alarm
        alarm_time should be a timezone aware datetime object.
        """
        url = "%s/%s/user/-/devices/tracker/%s/alarms.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            device_id
        )
        alarm_time = alarm_time.strftime("%H:%M%z")
        # Check week_days list
        if not isinstance(week_days, list):
            raise ValueError("Week days needs to be a list")
        for day in week_days:
            if day not in self.WEEK_DAYS:
                raise ValueError("Incorrect week day %s. see WEEK_DAY_LIST." % day)
        data = {
            'time': alarm_time,
            'weekDays': week_days,
            'recurring': recurring,
            'enabled': enabled,
            'vibe': vibe
        }
        if label:
            data['label'] = label
        if snooze_length:
            data['snoozeLength'] = snooze_length
        if snooze_count:
            data['snoozeCount'] = snooze_count
        return self.make_request(url, data=data, method="POST")
        # return

    def update_alarm(self, device_id, alarm_id, alarm_time, week_days, recurring=False, enabled=True, label=None,
                     snooze_length=None, snooze_count=None, vibe='DEFAULT'):
        """
        https://wiki.fitbit.com/display/API/API-Devices-Update-Alarm
        alarm_time should be a timezone aware datetime object.
        """
        # TODO Refactor with create_alarm. Tons of overlap.
        # Check week_days list
        if not isinstance(week_days, list):
            raise ValueError("Week days needs to be a list")
        for day in week_days:
            if day not in self.WEEK_DAYS:
                raise ValueError("Incorrect week day %s. see WEEK_DAY_LIST." % day)
        url = "%s/%s/user/-/devices/tracker/%s/alarms/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            device_id,
            alarm_id
        )
        alarm_time = alarm_time.strftime("%H:%M%z")

        data = {
            'time': alarm_time,
            'weekDays': week_days,
            'recurring': recurring,
            'enabled': enabled,
            'vibe': vibe
        }
        if label:
            data['label'] = label
        if snooze_length:
            data['snoozeLength'] = snooze_length
        if snooze_count:
            data['snoozeCount'] = snooze_count
        return self.make_request(url, data=data, method="POST")
        # return

    def delete_alarm(self, device_id, alarm_id):
        """
        https://wiki.fitbit.com/display/API/API-Devices-Delete-Alarm
        """
        url = "%s/%s/user/-/devices/tracker/%s/alarms/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            device_id,
            alarm_id
        )
        return self.make_request(url, method="DELETE")

    def get_sleep(self, date):
        """
        https://wiki.fitbit.com/display/API/API-Get-Sleep
        date should be a datetime.date object.
        """
        url = "%s/%s/user/-/sleep/date/%s-%s-%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            date.year,
            date.month,
            date.day
        )
        return self.make_request(url)

    def log_sleep(self, start_time, duration):
        """
        https://wiki.fitbit.com/display/API/API-Log-Sleep
        start time should be a datetime object. We will be using the year, month, day, hour, and minute.
        """
        data = {
            'startTime': start_time.strftime("%H:%M"),
            'duration': duration,
            'date': start_time.strftime("%Y-%m-%d"),
        }
        url = "%s/%s/user/-/sleep" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url, data=data, method="POST")

    def activities_list(self):
        """
        https://wiki.fitbit.com/display/API/API-Browse-Activities
        """
        url = "%s/%s/activities.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url)

    def activity_detail(self, activity_id):
        """
        https://wiki.fitbit.com/display/API/API-Get-Activity
        """
        url = "%s/%s/activities/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            activity_id
        )
        return self.make_request(url)

    def search_foods(self, query):
        """
        https://wiki.fitbit.com/display/API/API-Search-Foods
        """
        url = "%s/%s/foods/search.json?%s" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            urllib.urlencode({'query': query})
        )
        return self.make_request(url)

    def food_detail(self, food_id):
        """
        https://wiki.fitbit.com/display/API/API-Get-Food
        """
        url = "%s/%s/foods/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            food_id
        )
        return self.make_request(url)

    def food_units(self):
        """
        https://wiki.fitbit.com/display/API/API-Get-Food-Units
        """
        url = "%s/%s/foods/units.json" % (
            self.API_ENDPOINT,
            self.API_VERSION
        )
        return self.make_request(url)

    def get_bodyweight(self, base_date=None, user_id=None, period=None, end_date=None):
        """
        https://wiki.fitbit.com/display/API/API-Get-Body-Weight
        base_date should be a datetime.date object (defaults to today),
        period can be '1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max' or None
        end_date should be a datetime.date object, or None.

        You can specify period or end_date, or neither, but not both.
        """
        if not base_date:
            base_date = datetime.date.today()

        if not user_id:
            user_id = '-'

        if period and end_date:
            raise TypeError("Either end_date or period can be specified, not both")

        if not isinstance(base_date, basestring):
            base_date_string = base_date.strftime('%Y-%m-%d')
        else:
            base_date_string = base_date

        if period:
            if not period in ['1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']:
                raise ValueError("Period must be one of '1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max'")

            url = "%s/%s/user/%s/body/log/weight/date/%s/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
                period
            )
        elif end_date:
            if not isinstance(end_date, basestring):
                end_string = end_date.strftime('%Y-%m-%d')
            else:
                end_string = end_date

            url = "%s/%s/user/%s/body/log/weight/date/%s/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
                end_string
            )
        else:
            url = "%s/%s/user/%s/body/log/weight/date/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
            )
        return self.make_request(url)

    def get_bodyfat(self, base_date=None, user_id=None, period=None, end_date=None):
        """
        https://wiki.fitbit.com/display/API/API-Get-Body-fat
        base_date should be a datetime.date object (defaults to today),
        period can be '1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max' or None
        end_date should be a datetime.date object, or None.

        You can specify period or end_date, or neither, but not both.
        """
        if not base_date:
            base_date = datetime.date.today()

        if not user_id:
            user_id = '-'

        if period and end_date:
            raise TypeError("Either end_date or period can be specified, not both")

        if not isinstance(base_date, basestring):
            base_date_string = base_date.strftime('%Y-%m-%d')
        else:
            base_date_string = base_date

        if period:
            if not period in ['1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']:
                raise ValueError("Period must be one of '1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max'")

            url = "%s/%s/user/%s/body/log/fat/date/%s/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
                period
            )
        elif end_date:
            if not isinstance(end_date, basestring):
                end_string = end_date.strftime('%Y-%m-%d')
            else:
                end_string = end_date

            url = "%s/%s/user/%s/body/log/fat/date/%s/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
                end_string
            )
        else:
            url = "%s/%s/user/%s/body/log/fat/date/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                user_id,
                base_date_string,
            )
        return self.make_request(url)

    def get_friends(self, user_id=None):
        """
        https://wiki.fitbit.com/display/API/API-Get-Friends
        """
        if not user_id:
            user_id = '-'
        url = "%s/%s/user/%s/friends.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            user_id
        )
        return self.make_request(url)

    def get_friends_leaderboard(self, period):
        """
        https://wiki.fitbit.com/display/API/API-Get-Friends-Leaderboard
        """
        if not period in ['7d', '30d']:
            raise ValueError("Period must be one of '7d', '30d'")
        url = "%s/%s/user/-/friends/leaders/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            period
        )
        return self.make_request(url)

    def invite_friend(self, data):
        """
        https://wiki.fitbit.com/display/API/API-Create-Invite
        """
        url = "%s/%s/user/-/friends/invitations.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        return self.make_request(url, data=data)

    def invite_friend_by_email(self, email):
        """
        Convenience Method for
        https://wiki.fitbit.com/display/API/API-Create-Invite
        """
        return self.invite_friend({'invitedUserEmail': email})

    def invite_friend_by_userid(self, user_id):
        """
        Convenience Method for
        https://wiki.fitbit.com/display/API/API-Create-Invite
        """
        return self.invite_friend({'invitedUserId': user_id})

    def respond_to_invite(self, other_user_id, accept=True):
        """
        https://wiki.fitbit.com/display/API/API-Accept-Invite
        """
        url = "%s/%s/user/-/friends/invitations/%s.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            other_user_id,
        )
        accept = 'true' if accept else 'false'
        return self.make_request(url, data={'accept': accept})

    def accept_invite(self, other_user_id):
        """
        Convenience method for respond_to_invite
        """
        return self.respond_to_invite(other_user_id)

    def reject_invite(self, other_user_id):
        """
        Convenience method for respond_to_invite
        """
        return self.respond_to_invite(other_user_id, accept=False)

    def get_badges(self, user_id=None):
        """
        https://wiki.fitbit.com/display/API/API-Get-Badges
        """
        if not user_id:
            user_id = '-'
        url = "%s/%s/user/%s/badges.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            user_id
        )
        return self.make_request(url)

    def subscription(self, subscription_id, subscriber_id, collection=None,
                     method='POST'):
        """
        https://wiki.fitbit.com/display/API/Fitbit+Subscriptions+API
        """
        if not collection:
            url = "%s/%s/user/-/apiSubscriptions/%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                subscription_id
            )
        else:
            url = "%s/%s/user/-/%s/apiSubscriptions/%s-%s.json" % (
                self.API_ENDPOINT,
                self.API_VERSION,
                collection,
                subscription_id,
                collection
            )
        return self.make_request(
            url,
            method=method,
            headers={"X-Fitbit-Subscriber-id": subscriber_id}
        )

    def list_subscriptions(self, collection=''):
        """
        https://wiki.fitbit.com/display/API/Fitbit+Subscriptions+API
        """
        if collection:
            collection = '/%s' % collection
        url = "%s/%s/user/-%s/apiSubscriptions.json" % (
            self.API_ENDPOINT,
            self.API_VERSION,
            collection,
        )
        return self.make_request(url)

    @classmethod
    def from_oauth_keys(self, consumer_key, consumer_secret, user_key=None,
                        user_secret=None, user_id=None, system=US):
        client = FitbitOauthClient(consumer_key, consumer_secret, user_key,
                                   user_secret, user_id)
        return self(client, system)
    