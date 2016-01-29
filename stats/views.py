

from django.http.response import HttpResponse
from django.utils import simplejson
from physical.services.stats.services import PhysicalActivityDistributionService
from health.services.stats.services import HealthActivityDistributionService
from django.shortcuts import render_to_response
from django.template import RequestContext
from users.models import Profile
from physical.models import UserActivityLog
from nutrition.models import UserFoodLog
from health.models import UserSleepLog
from django.db.models.aggregates import Sum, Avg


def get_miles(request):
    dto = PhysicalActivityDistributionService().get_records_miles()
    
    return HttpResponse(simplejson.dumps(dto), mimetype="application/json")


def go_exercise_stats(request):
    total_dd_user = Profile.objects.count()
    total_exercise_log = UserActivityLog.objects.count()
    total_food_log = UserFoodLog.objects.count()
    total_sleep_log = UserSleepLog.objects.count()
    
    #Last_7_days miles
    dto_miles = PhysicalActivityDistributionService().get_records_miles_limit(days_offset=30)
    dto_hours = PhysicalActivityDistributionService().get_records_hour_limit(days_offset=30)
    #dto_steps = PhysicalActivityDistributionService()._get_global_distribution_steps_report_week()
    gender_m = Profile.objects.filter(gender="m").count()
    gender_f = Profile.objects.filter(gender="f").count()
    total_gender = gender_m + gender_f
    per_m = (gender_m * 100)/total_gender
    per_f = 100 - per_m
    gender = {"male":per_m, "female": per_f}
    #dto_sleep = HealthActivityDistributionService().get_global_distribution_sleep_month()
    #Last_7_days steps
    #Last_7_days hours
    
    #Gender distribution
    
    return render_to_response('stats/exercise.html',{"total_dd_users": total_dd_user,
                                                  "total_exercise_log": total_exercise_log,
                                                  "total_food_log": total_food_log,
                                                  "miles": dto_miles,
                                                  "hours": dto_hours,
                                                  #"steps": {},
                                                  "page": "exercise_stats",
                                                  "gender": gender,
                                                  "total_sleep_log": total_sleep_log},RequestContext(request))
    

def go_exercise_data(request):
    total_exercise_log = UserActivityLog.objects.all()[:100]
    
    return render_to_response('stats/exercise_row.html',{"logs": total_exercise_log, "page": "exercise_data",
                                                  },RequestContext(request))