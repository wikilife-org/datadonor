"""
//Miscellaneous
BiologicalSex = "gender"
BloodType = "blood_type"
DateOfBirth = "date_of_birth"
BodyTemperature = "body_temperature"

//Fitness
BodyMassIndex = "bmi"
Height = "height"
HeartRate = "heart_rate"
StepCount = "step_count"
Distance = "distance"
ActiveEnergy = "active_energy"
ActivityCount = "activity_count"
NikeFuel = "nike_fuel"

//Blood
OxygenSaturation = oxygen_saturation""
BloodGlucose = "blood_glucose"
BloodAlcoholContent = "blood_alcohol_Content"

//Nutrition
DietaryFatTotal = "fat_total"
DietaryFiber = "fiber"
DietarySugar = "sugar"
DietaryCalories = "calories"
DietaryProtein = "protein"
DietaryCarbohydrates = "carbohydrates"

"""
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.utils import simplejson
from users.models import Profile
import re, random, string


def authorize(request):
    result = {"message": "Authorize", "status": "success", "data":{}}
    username = "HK_%s"%''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    user = User.objects.create(username=username, password="", email="")
    user.profile.account_id
    data = {"userId":  user.profile.account_id}
    result["data"] = data
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

def oxygen_saturation(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def blood_glucose(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def blood_alcohol_content(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def blood_type(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def body_temperature(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def heart_rate(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def step_count(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def distance(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    
def activity_count(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def active_energy(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nike_fuel(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def bmi(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def fat_total(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def fiber(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def sugar(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def calories(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def protein(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def carbohydrates(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def height(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        user = Profile.objects.get(account_id=user_id).user
        value = request.POST["value"]
        date_ = request.POST["executeDateTime"]

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def gender(request):
    if request.method == 'POST':
        user_id = request.POST["userId"]
        value = request.POST["value"]
        profile = Profile.objects.get(account_id=user_id)
        profile.gender = value
        profile.save()
        data = {"message": "Gender", "status": "success", "data":{}}
    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def date_of_birth(request):
    
    if request.method == 'POST':
        user_id = request.POST["userId"]
        value = request.POST["value"]
        profile = Profile.objects.get(account_id=user_id)
        profile.date_of_birth = value
        profile.save()
        data = {"message": "DateOdBirth", "status": "success", "data":{}}

    else:
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
