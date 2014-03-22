# coding=utf-8

from django.http.response import HttpResponse
from django.utils import simplejson
from physical.services.stats.services import PhysicalActivityDistributionService,\
    PhysicalActivityService


def physical_exercise(request):
    """
    data = [{"title": "Running", "key":"running", "global_times":4, "user_times":5 }, 
     {"title": "Walking", "key":"walking", "global_times":3, "user_times":1 },
     {"title": "Eliptical", "key":"Eliptical", "global_times":1, "user_times": 2}]
    """

    user_id = request.user.id 
    dto = PhysicalActivityService().get_top_activities(user_id)
    data = [
            {"title": dto[0]["act_name"], "key": dto[0]["act_wl_id"], "global_times": dto[0]["global_tpw"], "user_times": dto[0]["user_tpw"]}, 
            {"title": dto[1]["act_name"], "key": dto[1]["act_wl_id"], "global_times": dto[1]["global_tpw"], "user_times": dto[1]["user_tpw"]}, 
            {"title": dto[2]["act_name"], "key": dto[2]["act_wl_id"], "global_times": dto[2]["global_tpw"], "user_times": dto[2]["user_tpw"]} 
    ]

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_user_exercise(request):
    
    data = [{"title": "Bike riding", "message":"every day"}, 
     {"title": "Snowboard", "message":"1 time per week"},
     {"title": "Downhill Skiing", "message":"1 times per year"},
     {"title": "Weight lifting", "message":"4 per year"}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_steps_distribution(request):
    """
    data = {"days":{"sunday":{"user_steps": 4000, "global_steps":2000}, "monday":{"user_steps": 3000, "global_steps":1000},
                    "tuesday":{"user_steps": 3000, "global_steps":1000}, "wednesday":{"user_steps": 3000, "global_steps":3000},
                    "thursday":{"user_steps": 5000, "global_steps":3000}, "friday":{"user_steps": 3000, "global_steps":2000},
                    "saturday":{"user_steps": 5000, "global_steps":3050}},
            "global_avg_steps":3000,
            "user_avg_steps": 2000}
    """
    user_id = request.user.id 
    dto = PhysicalActivityDistributionService().get_steps_distribution(user_id)
    data = {
            "days": {
                     "sunday":    {"user_steps": dto["sun"]["user"], "global_steps": dto["sun"]["global"]}, 
                     "monday":    {"user_steps": dto["mon"]["user"], "global_steps": dto["mon"]["global"]},
                     "tuesday":   {"user_steps": dto["tue"]["user"], "global_steps": dto["tue"]["global"]}, 
                     "wednesday": {"user_steps": dto["wed"]["user"], "global_steps": dto["wed"]["global"]},
                     "thursday":  {"user_steps": dto["thu"]["user"], "global_steps": dto["thu"]["global"]}, 
                     "friday":    {"user_steps": dto["fri"]["user"], "global_steps": dto["fri"]["global"]},
                     "saturday":  {"user_steps": dto["sat"]["user"], "global_steps": dto["sat"]["global"]}
                     },
            "global_avg_steps": dto["avg"]["global"],
            "user_avg_steps":   dto["avg"]["user"]
    }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_miles_distribution(request):
    """
    data = {"days":{"sunday":{"user_miles": 30, "global_miles":50}, "monday":{"user_miles": 20, "global_miles":30},
                    "tuesday":{"user_miles": 30, "global_miles":40}, "wednesday":{"user_miles": 12, "global_miles":20},
                    "thursday":{"user_miles": 30, "global_miles":50}, "friday":{"user_miles": 15, "global_miles":10},
                    "saturday":{"user_miles": 30, "global_miles":60}},
            "global_avg_miles":30,
            "user_avg_miles": 20}
    """
    user = request.user 
    dto = PhysicalActivityDistributionService().get_miles_distribution(user)
    data = {
            "days": {
                     "sunday":    {"user_miles": dto["sun"]["user"], "global_miles": dto["sun"]["global"]}, 
                     "monday":    {"user_miles": dto["mon"]["user"], "global_miles": dto["mon"]["global"]},
                     "tuesday":   {"user_miles": dto["tue"]["user"], "global_miles": dto["tue"]["global"]}, 
                     "wednesday": {"user_miles": dto["wed"]["user"], "global_miles": dto["wed"]["global"]},
                     "thursday":  {"user_miles": dto["thu"]["user"], "global_miles": dto["thu"]["global"]}, 
                     "friday":    {"user_miles": dto["fri"]["user"], "global_miles": dto["fri"]["global"]},
                     "saturday":  {"user_miles": dto["sat"]["user"], "global_miles": dto["sat"]["global"]}
                     },
            "global_avg_miles": dto["avg"]["global"],
            "user_avg_miles":   dto["avg"]["user"]
    }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_hours_distribution(request):
    """
    data = {"days":{"sunday":{"user_hours": 7, "global_hours":7}, "monday":{"user_hours": 3, "global_hours":5},
                    "tuesday":{"user_hours": 3, "global_hours":5}, "wednesday":{"user_hours": 4, "global_hours":6},
                    "thursday":{"user_hours": 5, "global_hours":5}, "friday":{"user_hours": 4, "global_hours":4},
                    "saturday":{"user_hours": 6, "global_hours":6}},
            "global_avg_hours":4,
            "user_avg_hours": 5}
    """
    user_id = request.user.id 
    dto = PhysicalActivityDistributionService().get_steps_distribution(user_id)
    data = {
            "days": {
                     "sunday":    {"user_hours": dto["sun"]["user"], "global_hours": dto["sun"]["global"]}, 
                     "monday":    {"user_hours": dto["mon"]["user"], "global_hours": dto["mon"]["global"]},
                     "tuesday":   {"user_hours": dto["tue"]["user"], "global_hours": dto["tue"]["global"]}, 
                     "wednesday": {"user_hours": dto["wed"]["user"], "global_hours": dto["wed"]["global"]},
                     "thursday":  {"user_hours": dto["thu"]["user"], "global_hours": dto["thu"]["global"]}, 
                     "friday":    {"user_hours": dto["fri"]["user"], "global_hours": dto["fri"]["global"]},
                     "saturday":  {"user_hours": dto["sat"]["user"], "global_hours": dto["sat"]["global"]}
                     },
            "global_avg_hours": dto["avg"]["global"],
            "user_avg_hours":   dto["avg"]["user"]
    }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


## Mocks ###


def physical_exercise_mock(request):

    data = [{"title": "Running", "key":"running", "global_times":4, "user_times":5 }, 
     {"title": "Walking", "key":"walking", "global_times":3, "user_times":1 },
     {"title": "Eliptical", "key":"Eliptical", "global_times":1, "user_times": 2}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_user_exercise_mock(request):

    data = [{"title": "Bike riding", "message":"every day"}, 
     {"title": "Snowboard", "message":"1 time per week"},
     {"title": "Downhill Skiing", "message":"1 times per year"},
     {"title": "Weight lifting", "message":"4 per year"}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_steps_distribution_mock(request):
    data = {"days":{"sunday":{"user_steps": 4000, "global_steps":2000}, "monday":{"user_steps": 3000, "global_steps":1000},
                    "tuesday":{"user_steps": 3000, "global_steps":1000}, "wednesday":{"user_steps": 3000, "global_steps":3000},
                    "thursday":{"user_steps": 5000, "global_steps":3000}, "friday":{"user_steps": 3000, "global_steps":2000},
                    "saturday":{"user_steps": 5000, "global_steps":3050}},
            "global_avg_steps":3000,
            "user_avg_steps": 2000}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_miles_distribution_mock(request):
    data = {"days":{"sunday":{"user_miles": 30, "global_miles":50}, "monday":{"user_miles": 20, "global_miles":30},
                    "tuesday":{"user_miles": 30, "global_miles":40}, "wednesday":{"user_miles": 12, "global_miles":20},
                    "thursday":{"user_miles": 30, "global_miles":50}, "friday":{"user_miles": 15, "global_miles":10},
                    "saturday":{"user_miles": 30, "global_miles":60}},
            "global_avg_miles":30,
            "user_avg_miles": 20}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_hours_distribution_mock(request):
    data = {"days":{"sunday":{"user_hours": 7, "global_hours":7}, "monday":{"user_hours": 3, "global_hours":5},
                    "tuesday":{"user_hours": 3, "global_hours":5}, "wednesday":{"user_hours": 4, "global_hours":6},
                    "thursday":{"user_hours": 5, "global_hours":5}, "friday":{"user_hours": 4, "global_hours":4},
                    "saturday":{"user_hours": 6, "global_hours":6}},
            "global_avg_hours":4,
            "user_avg_hours": 5}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
