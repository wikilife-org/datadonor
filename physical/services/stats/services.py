# coding=utf-8

"""
This services are used by the views
"""

import datetime
from physical.models import RUNNING_WL_ACT_ID, WALKING_WL_ACT_ID,\
    ELLIPTICAL_WL_ACT_ID, GlobalPhysicalActivity, UserPhysicalActivity,\
    UserDistributionLastWeek, GlobalDistributionLastWeek, STEPS_ACT_CODE,\
    MILES_ACT_CODE, HOURS_ACT_CODE

from wikilife.clients.stats import Stats


class PhysicalActivityDistributionService(object):

    def get_steps_distribution(self, user):
        return self._get_global_distribution_steps(user)

    def get_miles_distribution(self, user):
        return self._get_global_distribution_miles(user)

    def get_hours_distribution(self, user):
        return self._get_global_distribution_hours(user)


    def _get_global_distribution_steps(self, user):
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_steps_from_sunday()["data"]
        result = {"sun":{"user":0, "global":0},"mon":{"user":0, "global":0},"tue":{"user":0, "global":0},"wed":{"user":0, "global":0},
                  "thu":{"user":0, "global":0},"fri":{"user":0, "global":0},"sat":{"user":0, "global":0}, "avg":{"user":0, "global":0}}
        total = 0
        count = 0
        avg = 0
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index]["global"] = int(round(day["avg"]))
            
            total +=day["avg"]
            count = count + 1
        if count:
            avg = total/ count
        result["avg"]["global"] = int(round(avg))
        return result

    def _get_global_distribution_miles(self, user):
        #Wikilife Retunrs KM, we should convert it to Miles
        MILES_FACTOR = 0.621371192
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_distance_from_sunday()["data"]
        result = {"sun":{"user":0, "global":0},"mon":{"user":0, "global":0},"tue":{"user":0, "global":0},"wed":{"user":0, "global":0},
                  "thu":{"user":0, "global":0},"fri":{"user":0, "global":0},"sat":{"user":0, "global":0}, "avg":{"user":0, "global":0}}
        total = 0
        count = 0
        avg = 0
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index]["global"] = int(round(day["avg"] * MILES_FACTOR))
            
            total +=int(round(day["avg"] * MILES_FACTOR))
            count = count + 1
        if count:
            avg = total/ count
        result["avg"]["global"] = int(round(avg))
        return result

    def _get_global_distribution_hours(self, user):
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_steps_from_sunday()["data"]
        result = {"sun":{"user":0, "global":0},"mon":{"user":0, "global":0},"tue":{"user":0, "global":0},"wed":{"user":0, "global":0},
                  "thu":{"user":0, "global":0},"fri":{"user":0, "global":0},"sat":{"user":0, "global":0}, "avg":{"user":0, "global":0}}
        
        
        return result
    
        """total = 0
        count = 0
        avg = 0
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index]["global"] = int(round(day["avg"]))
            
            total +=day["avg"]
            count = count + 1
        if count:
            avg = total/ count
        result["avg"]["global"] = int(round(avg))
        return result"""
    
    def _get_user_distribution(self, user, act_code):
        try:
            act_dist = UserDistributionLastWeek.objects.get(user=user, act_code=act_code)
        except:
            act_dist = UserDistributionLastWeek()

        return act_dist


class PhysicalActivityService(object):

    def get_top_activities(self, user):
        """
        Returns first two top de facto global activities (Running, Walking), even if the user has no participation in them, 
        and a third activity representing the user top activity, unless is one of the first two 
        in which case will return the next user top activity.
        If user has no data the three top de facto global activities (Running, Walking, Eliptical) are returned.
        
        [
            {
                act_name: "",
                global_tpw: 0,
                user_tpw: 0
            },
            {
                act_name: "",
                global_tpw: 0,
                user_tpw: 0
            },
            {
                act_name: "",
                global_tpw: 0,
                user_tpw: 0
            }
        ]
        """
        running_act = self._get_global_activity(RUNNING_WL_ACT_ID, "Running")
        walking_act = self._get_global_activity(WALKING_WL_ACT_ID, "Walking")
        eliptical_act = self._get_global_activity(ELLIPTICAL_WL_ACT_ID, "Eliptical")

        running_act["user_tpw"] = self._get_user_tpw_by_act_id(user, RUNNING_WL_ACT_ID)
        walking_act["user_tpw"] = self._get_user_tpw_by_act_id(user, WALKING_WL_ACT_ID)
        eliptical_act["user_tpw"] = self._get_user_tpw_by_act_id(user, ELLIPTICAL_WL_ACT_ID)

        top_activities = [running_act, walking_act, eliptical_act]

        """if running_act["user_tpw"]>0 or walking_act["user_tpw"]>0 or eliptical_act["user_tpw"]>0:
            top_activities.append(eliptical_act)
        else:
            top_user_activity = self._get_user_top_activity(user_id)
            if top_user_activity!=None: 
                top_user_act = self._get_global_activity(top_user_activity.act_wl_id)
                top_user_act["user_tpw"] = top_user_activity.tpw 
                top_activities.append(top_user_act)
            else:
                top_activities.append(eliptical_act)"""

        return top_activities

    def _get_global_activity(self, act_wl_id):
        global_act = GlobalPhysicalActivity.objects.get(act_wl_id=act_wl_id)

        if global_act==None or (datetime.datetime.now()-global_act.update_time).days > 1:
            global_act.tpw = self._get_wl_global_act_tpw(act_wl_id)
            global_act.save()

        act = {}
        act["act_name"] = global_act.name 
        act["act_wl_id"] = act_wl_id 
        act["global_tpw"] = global_act.tpw 

        return act


    def _get_global_activity(self, act_wl_id, title):
        client = Stats({"HOST":"http://localhost:7080"})
        tpw = client.get_times_per_week_by_id(act_wl_id)["data"]
        act = {}
        act["act_name"] = title
        act["act_wl_id"] = act_wl_id 
        act["global_tpw"] = tpw

        return act
    
    def _get_wl_global_act_tpw(self, act_wl_id):
        #self._wl_stat_client.get_ ???
        return 0

    def _get_user_tpw_by_act_id(self, user, act_id):
        return 0
        """ act = UserPhysicalActivity.objects.get(user=user, act_wl_id=act_id)
        if act!=None:
            return act.tpw

        return 0 """

    def _get_user_top_activity(self, user_id):
        acts = UserPhysicalActivity.objects.filter(user_id=user_id).order_by("tpw")
        if acts.size()>0:
            return acts[0]

        return None
