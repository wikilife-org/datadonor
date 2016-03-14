

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
                                                  "section": "exercise",
                                                  "total_sleep_log": total_sleep_log},RequestContext(request))
    

def go_exercise_data(request):
    total_exercise_log = UserActivityLog.objects.all().order_by("-execute_time")[:100]
    
    return render_to_response('stats/exercise_row.html',{"logs": total_exercise_log, "page": "exercise_data",
                                                  },RequestContext(request))
    
from health.utilities import get_conditions_rank, get_complaints_rank, get_emotions_rank, global_blood_type
from health.models import UserConditions, UserBloodType, UserComplaints, UserEmotions


def go_health_stats(request):
    condition_rank, total_conditions = get_conditions_rank()
    complaints_rank, total_complaints = get_complaints_rank()
    emotions_rank, total_emotions = get_emotions_rank()
    total_conditions_logs = UserConditions.objects.all().count()
    total_complaints_logs = UserComplaints.objects.all().count()
    total_blood_type_logs = UserBloodType.objects.all().count()
    total_emotions_logs = UserEmotions.objects.all().count()
    blood_types = global_blood_type()
    
    for blood in blood_types:
        blood["percentage"] = "%s"%round(blood["percentage"], 2)

    
    return render_to_response('stats/health.html',{"condition_rank": condition_rank[:5],
                                                  "complaints_rank": complaints_rank[:5],
                                                  "emotions_rank": emotions_rank[:5],
                                                  "blood_types": blood_types,
                                                  "total_conditions_logs": total_conditions_logs,
                                                  "total_complaints_logs": total_complaints_logs,
                                                  "total_blood_type_logs": total_blood_type_logs,
                                                  "total_emotions_logs": total_emotions_logs,
                                                  "page": "health_stats",
                                                  "section": "health",
                                                  },RequestContext(request))
    
    
def go_health_data(request):
    condition_rank, total_conditions = get_conditions_rank()
    complaints_rank, total_complaints = get_complaints_rank()
    emotions_rank, total_emotions = get_emotions_rank()
    
    condition_report = condition_rank[:30]
    for condition in condition_report:
        condition["percentage"] = "%s"%round(condition["percentage"], 2)
    
    complaints_report = complaints_rank[:30]
    for complaints in complaints_report:
        complaints["percentage"] = "%s"%round(complaints["percentage"], 2)
    
    emotion_report = emotions_rank[:30]
    for  emotion in emotion_report:
        emotion["percentage"] = "%s"%round(emotion["percentage"], 2)
    
    return render_to_response('stats/health_row.html',{"conditions": condition_report,
                                                       "complaints": complaints_report,
                                                       "emotions": emotion_report,
                                                        "page": "health_data",
                                                        "section": "health",
                                                  },RequestContext(request))
    
    

from nutrition.services.utilities import get_global_bmi, global_weight, global_height
from nutrition.models import UserFoodLog
from nutrition.services.stats.services import NutritionDistributionService
from users.models import Profile

def go_nutrition_stats(request):
    # nutrients distribution
    # BMI gender distribution
    # Cant logs
    total_logs = UserFoodLog.objects.count()
    bmi = get_global_bmi()
    bmi_users_cant = Profile.objects.filter(weight__isnull =  False).count()
    bmi_dto = [{"x":'Men', "y": bmi["men"]["value"] },  {"x":'Women', "y": bmi["women"]["value"] }]
    data = NutritionDistributionService().get_nutrients_global_distribution(delta=100)
    print data
    return render_to_response('stats/nutrition.html',{
                                                    'bmi_based': bmi_users_cant,
                                                  "total_nutrition_logs": total_logs,
                                                  'data': data,
                                                  "bmi": bmi_dto,
                                                  "page": "nutrition_stats",
                                                  "section": "nutrition",
                                                  },RequestContext(request))


def go_nutrition_data(request):
    logs = UserFoodLog.objects.all()
    return render_to_response('stats/nutrition_row.html',{
                                                        "page": "nutrition_data",
                                                        "section": "nutrition",
                                                        "logs": logs,
                                                  },RequestContext(request))