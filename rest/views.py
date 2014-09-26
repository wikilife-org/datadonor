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


def validate(request):
    pass

def create_user(request):
    pass

def profile(request):
    if request.method == 'POST':
        request.POST["user_id"]
        user = Users.objects.get(id=user_id)
        #Get profile from user
        request.POST["height"]
        request.POST["gender"]
        request.POST["date_of_birth"]
        request.POST["date"]

    else:
        #validate
        pass

def physical(request):
    if request.method == 'POST':
        request.POST["user_id"]
        request.POST["heart_rate"]
        request.POST["step_count"]
        request.POST["distance"]
        request.POST["activity_count"]
        request.POST["active_energy"]
        request.POST["nike_fuel"]
        request.POST["date"]
    else:
        #validate
        pass


def health(request):
    if request.method == 'POST':
        request.POST["user_id"]
        request.POST["oxygen_saturation"]
        request.POST["blood_glucose"]
        request.POST["blood_alcohol_Content"]
        request.POST["blood_type"]
        request.POST["body_temperature"]
        request.POST["date"]
    else:
        pass

def nutrition(request):
    if request.method == 'POST':
        request.POST["user_id"]
        request.POST["bmi"]
        request.POST["fat_total"]
        request.POST["fiber"]
        request.POST["sugar"]
        request.POST["calories"]
        request.POST["protein"]
        request.POST["carbohydrates"]
        request.POST["date"]
    else:
        pass