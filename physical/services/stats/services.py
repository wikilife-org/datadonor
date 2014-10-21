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
from physical.models import UserActivityLog
from utils.date_util import get_last_sunday_list_days
from django.db.models.aggregates import Sum, Avg

class PhysicalActivityDistributionService(object):

    def get_steps_distribution(self, user):
        return self._get_global_distribution_steps(user)
    
    def get_steps_distribution_global(self):
        return self._get_global_distribution_steps_report()
    
    def get_miles_distribution(self, user):
        return self._get_global_distribution_miles(user)
    
    def get_miles_distribution_global(self):
        return self._get_global_distribution_miles_report()
    
    def get_hours_distribution(self, user):
        return self._get_global_distribution_hours(user)

    def get_hours_distribution_global(self):
        return self._get_global_distribution_hours_report()
    
    def _get_user_distribution_info(self, user, q, result):
        total_user = 0 
        count_user = 0
        avg_user = 0
        
        sum_id = "%s__sum"%q
        day_list = get_last_sunday_list_days()
        for day in day_list:
            
            values = UserActivityLog.objects.filter(user=user, type__in=["walking", "running", "cycling"], execute_time=day).aggregate(Sum(q))
            value = values[sum_id] or 0
            total_user +=value
            count_user = count_user + 1
            d_index = day.strftime("%a").lower()
            result[d_index]["user"] = value
        
        if count_user:
            avg_user = total_user/ count_user
        result["avg"]["user"] = int(round(avg_user))
        return result 

    def _get_global_distribution_steps_report(self):

        
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_steps_from_sunday()["data"]
        result = {"sun":None,"mon":None,"tue":None,"wed":None,
                  "thu":None,"fri":None,"sat":None, "avg":None}
        total = 0
        count = 0
        avg = 0
        entries = 0
        
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index] = int(round(day["avg"]))
            entries += int(day["entries"])
            total +=day["avg"]
            count = count + 1
        if count:
            avg = total/ count
        result["avg"] = int(round(avg))
        result["total_users"] = entries
        return result
    
    def _get_global_distribution_steps(self, user):

        
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_steps_from_sunday()["data"]
        result = {"sun":{"user":0, "global":0},"mon":{"user":0, "global":0},"tue":{"user":0, "global":0},"wed":{"user":0, "global":0},
                  "thu":{"user":0, "global":0},"fri":{"user":0, "global":0},"sat":{"user":0, "global":0}, "avg":{"user":0, "global":0}}
        total = 0
        count = 0
        avg = 0
        
        result = self._get_user_distribution_info(user, "steps",result)

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
        
        result = self._get_user_distribution_info(user, "miles",result)
        
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index]["global"] = int(round(day["avg"] * MILES_FACTOR))
            
            total +=int(round(day["avg"] * MILES_FACTOR))
            count = count + 1
        if count:
            avg = total/ count
        result["avg"]["global"] = int(round(avg))
        return result


    def _get_global_distribution_miles_report(self):

        
        client = Stats({"HOST":"http://api.wikilife.org"})
        steps_days = client.get_global_distance_from_sunday()["data"]
        result = {"sun":None,"mon":None,"tue":None,"wed":None,
                  "thu":None,"fri":None,"sat":None, "avg":None}
        total = 0
        count = 0
        avg = 0
        entries = 0
        
        for day in steps_days:
            d_index = datetime.datetime.strptime(day["date"], '%Y-%m-%d').strftime("%a").lower()
            result[d_index] = int(round(day["avg"]))
            entries +=int(day["entries"])
            total +=day["avg"]
            count = count + 1
        if count:
            avg = total/ count
        result["avg"] = int(round(avg))
        result["total_users"] = entries
        return result
    
    def _get_global_distribution_hours(self, user):
        client = Stats({"HOST":"http://api.wikilife.org"})
        #steps_days = client.get_global_steps_from_sunday()["data"]
        #aggregation in DD
        
        result = {"sun":{"user":0, "global":0},"mon":{"user":0, "global":0},"tue":{"user":0, "global":0},"wed":{"user":0, "global":0},
                  "thu":{"user":0, "global":0},"fri":{"user":0, "global":0},"sat":{"user":0, "global":0}, "avg":{"user":0, "global":0}}
        total = 0 
        count = 0
        avg = 0
        
        h_id = "hours__sum"
        day_list = get_last_sunday_list_days()
        for day in day_list:
            
            values = UserActivityLog.objects.filter(execute_time=day, type__in=["walking", "running", "cycling"]).aggregate(Sum("hours"))
            count = UserActivityLog.objects.filter(execute_time=day, type__in=["walking", "running", "cycling"]).values_list('user', flat=True).distinct().count()
            value = values[h_id] or 0
            
            d_index = day.strftime("%a").lower()
            avg_ = 0
            if count:
                avg_ = round(value / count)
            total +=avg_
            result[d_index]["global"] = avg_
        
        if len(day_list):
            avg = total/ len(day_list)
        result["avg"]["global"] = int(round(avg))
        result = self._get_user_distribution_info(user, "hours",result)
        
        return result
    
    def _get_global_distribution_hours_report(self):


        result = {"sun":None,"mon":None,"tue":None,"wed":None,
                  "thu":None,"fri":None,"sat":None, "avg":None}
        total = 0 
        count = 0
        avg = 0
        total_users = 0
        
        h_id = "hours__sum"
        day_list = get_last_sunday_list_days()
        for day in day_list:
            
            values = UserActivityLog.objects.filter(execute_time=day, type__in=["walking", "running", "cycling"]).aggregate(Sum("hours"))
            count = UserActivityLog.objects.filter(execute_time=day, type__in=["walking", "running", "cycling"]).values_list('user', flat=True).distinct().count()
            value = values[h_id] or 0
            
            d_index = day.strftime("%a").lower()
            avg_ = 0
            if count:
                avg_ = round(value / count)
                total_users +=count
            total +=avg_
            result[d_index] = avg_
        
        if len(day_list):
            avg = total/ len(day_list)
        result["avg"] = int(round(avg))
        result["total_users"] = total_users
        
        return result

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

        running_act["user_tpw"] = self._get_user_tpw_by_act_id(user, "running")
        walking_act["user_tpw"] = self._get_user_tpw_by_act_id(user, "walking")
        eliptical_act["user_tpw"] = self._get_user_tpw_by_act_id(user, "eliptical")

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
        client = Stats({"HOST":"http://api.wikilife.org"})
        tpw = client.get_times_per_week_by_id(act_wl_id)["data"]
        act = {}
        act["act_name"] = title
        act["act_wl_id"] = act_wl_id 
        act["global_tpw"] = int(round(tpw))

        return act
    
    def _get_wl_global_act_tpw(self, act_wl_id):
        #self._wl_stat_client.get_ ???
        return 0
    
    
    
    def _get_user_tpw_by_act_id(self, user, act_id):
        #filter by date today - 7
        d=datetime.date.today()-datetime.timedelta(days=7)
        total = UserActivityLog.objects.filter(user=user, type=act_id, execute_time__range=[d, datetime.date.today()]).count()
        return total
        """ act = UserPhysicalActivity.objects.get(user=user, act_wl_id=act_id)
        if act!=None:
            return act.tpw

        return 0 """

    def _get_user_top_activity(self, user_id):
        acts = UserPhysicalActivity.objects.filter(user_id=user_id).order_by("tpw")
        if acts.size()>0:
            return acts[0]

        return None
