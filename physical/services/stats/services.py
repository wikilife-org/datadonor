# coding=utf-8

"""
This services are used by the views
"""

import datetime
from physical.models import RUNNING_WL_ACT_ID, WALKING_WL_ACT_ID,\
    ELLIPTICAL_WL_ACT_ID, GlobalPhysicalActivity, UserPhysicalActivity,\
    UserDistributionLastWeek, GlobalDistributionLastWeek, STEPS_ACT_CODE,\
    MILES_ACT_CODE, HOURS_ACT_CODE


class PhysicalActivityDistributionService(object):

    def get_steps_distribution(self, user_id):
        return self._get_distribution(user_id, STEPS_ACT_CODE)

    def get_miles_distribution(self, user_id):
        return self._get_distribution(user_id, MILES_ACT_CODE)

    def get_hours_distribution(self, user_id):
        return self._get_distribution(user_id, HOURS_ACT_CODE)

    def _get_distribution(self, user_id, act_code):
        global_dist = self._get_global_distribution(act_code)
        user_dist = self._get_user_distribution(user_id, act_code)

        r = {
             "sun": {"user": user_dist.sun, "global": global_dist.sun},
             "mon": {"user": user_dist.mon, "global": global_dist.mon},
             "tue": {"user": user_dist.tue, "global": global_dist.tue},
             "wed": {"user": user_dist.wed, "global": global_dist.wed},
             "thu": {"user": user_dist.thu, "global": global_dist.thu},
             "fri": {"user": user_dist.fri, "global": global_dist.fri},
             "sat": {"user": user_dist.sat, "global": global_dist.sat},
             "avg": {"user": user_dist.avg, "global": global_dist.avg}
        }
        return r

    def _get_global_distribution(self, act_code):
        act_dist = GlobalDistributionLastWeek.objects.get(act_code=act_code)

        if act_dist==None or (datetime.datetime.now()-act_dist.update_time).days > 1:
            #TODO get from WL
            pass

        return act_dist

    def _get_user_distribution(self, user_id, act_code):
        act_dist = UserDistributionLastWeek.objects.get(user_id=user_id, act_code=act_code)
        if act_dist==None:
            act_dist = UserDistributionLastWeek()

        return act_dist


class PhysicalActivityService(object):

    def get_top_activities(self, user_id):
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
        running_act = self._get_global_activity(RUNNING_WL_ACT_ID)
        walking_act = self._get_global_activity(WALKING_WL_ACT_ID)
        eliptical_act = self._get_global_activity(ELLIPTICAL_WL_ACT_ID)

        running_act["user_tpw"] = self._get_user_tpw_by_act_id(user_id, RUNNING_WL_ACT_ID)
        walking_act["user_tpw"] = self._get_user_tpw_by_act_id(user_id, WALKING_WL_ACT_ID)
        eliptical_act["user_tpw"] = self._get_user_tpw_by_act_id(user_id, ELLIPTICAL_WL_ACT_ID)

        top_activities = [running_act, walking_act]

        if running_act["user_tpw"]>0 or walking_act["user_tpw"]>0 or eliptical_act["user_tpw"]>0:
            top_activities.append(eliptical_act)
        else:
            top_user_activity = self._get_user_top_activity(user_id)
            if top_user_activity!=None: 
                top_user_act = self._get_global_activity(top_user_activity.act_wl_id)
                top_user_act["user_tpw"] = top_user_activity.tpw 
                top_activities.append(top_user_act)
            else:
                top_activities.append(eliptical_act)

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

    def _get_wl_global_act_tpw(self, act_wl_id):
        #self._wl_stat_client.get_ ???
        return 0

    def _get_user_tpw_by_act_id(self, user_id, act_id):
        act = UserPhysicalActivity.objects.get(user_id=user_id, act_wl_id=act_id)
        if act!=None:
            return act.tpw

        return 0 

    def _get_user_top_activity(self, user_id):
        acts = UserPhysicalActivity.objects.filter(user_id=user_id).order_by("tpw")
        if acts.size()>0:
            return acts[0]

        return None
