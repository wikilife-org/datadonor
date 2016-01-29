# coding=utf-8

"""
This services are used by the views
"""

import datetime
from health.models import UserSleepLog, UserMoodLastWeek
from health.clients.mood_panda import MoodPandaClient
from utils.date_util import get_last_sunday_list_days
from django.db.models.aggregates import Sum, Avg

class HealthActivityDistributionService(object):
    
    def get_user_distribution_sleep(self, user):
        result = {"days":{"sunday":{"hours": 0}, "monday":{"hours": 0 },
                    "tuesday":{"hours": 0 }, "wednesday":{"hours": 0 },
                    "thursday":{"hours": 0 }, "friday":{"hours": 0},
                    "saturday":{"hours": 0}},
            "avg_hours":0}
        total_user = 0 
        count_user = 0
        avg_user = 0
        
        sum_id = "minutes__sum"
        day_list = get_last_sunday_list_days()
        for day in day_list:
            
            values = UserSleepLog.objects.filter(user=user, execute_time=day).aggregate(Sum("minutes"))
            value = values[sum_id] or 0
            total_user +=value
            count_user = count_user + 1
            d_index = day.strftime("%A").lower()
            result["days"][d_index]["hours"] = round(value/60, 1)
        
        if count_user:
            avg_user = total_user/ count_user
        result["avg_hours"] = round(avg_user/60, 1)
        return result 


    def get_global_distribution_sleep(self):
        result = {"days":{"sunday":{"hours": 0}, "monday":{"hours": 0 },
                    "tuesday":{"hours": 0 }, "wednesday":{"hours": 0 },
                    "thursday":{"hours": 0 }, "friday":{"hours": 0},
                    "saturday":{"hours": 0}},
            "avg_hours":0}
        total_user = 0 
        count_user = 0
        avg_user = 0
        global_avg = 0
        
        sum_id = "minutes__sum"
        day_list = get_last_sunday_list_days()
        for day in day_list:
            
            values = UserSleepLog.objects.filter(execute_time=day).aggregate(Sum("minutes"))
            value = values[sum_id] or 0
            
            count_user = UserSleepLog.objects.filter(execute_time=day).values_list('user', flat=True).distinct().count()
            d_index = day.strftime("%A").lower()
            global_avg = 0
            if count_user:
                global_avg =  round((value/60) /count_user, 1)
            result["days"][d_index]["hours"] = global_avg
            total_user +=global_avg
        
        if len(day_list):
            avg_user = total_user/ len(day_list)
        result["avg_hours"] = round(avg_user, 1)
        return result 
    
    def get_global_distribution_sleep_month(self, year=2015, months=[(1,"Jan"),(2,"Feb"),(3,"Mar"),(4,"Apr"),(5,"May")\
                                                                     ,(6,"Jun"),(7,"Jul"),(8,"Aug"),(9,"Sep"),(10,"Oct"),(11,"Nov"), (12, "Dec")]):
        result = {}
        data = []
        total_avg = 0 
        count_user = 0
        global_avg = 0
        
        sum_id = "minutes__sum"
        for month in months:
            values = UserSleepLog.objects.filter(execute_time__month=month[0], execute_time__year=year).aggregate(Sum("minutes"))   
            value = values[sum_id] or 0
            
            count_user = UserSleepLog.objects.filter(execute_time__month=month[0], execute_time__year=year).values_list('user', flat=True).count()
            global_avg = 0
            if count_user:
                global_avg =  round(value/60/count_user, 1)
            data.append({"x": month[1], "y": global_avg}) 
            total_avg +=global_avg
        
        
        result["data"] = data
        result["avg_sleep"] = round(total_avg/12, 1)
        return result 
    
    def get_mood_from_moodpanda(self, user):
        
        user_email = user.profile.email
        client = MoodPandaClient(user_email=user_email)
        mood = client.get_avg_mood_last_30_days()
        try:
            obj = UserMoodLastWeek.objects.get(user=user)
            obj.avg_mood = mood
            obj.save()
        except:
            obj = UserMoodLastWeek.objects.create(user=user, avg_mood=mood)

            
        
        