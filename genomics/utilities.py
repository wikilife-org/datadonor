
from django.utils.translation import gettext as _
import math
from utils.commons import percentage
from social_auth.models import *
from datetime import date
from users.models import Profile
from genomics.models import *
from utils.commons import percentage
from operator import itemgetter

def order_list(l,v):
    if l[1]["name"] != v:
         aux_0 = l[1]
         aux_1 = l[0]
         l[0] = aux_0
         l[1] = aux_1

def get_traits_alcohol_distribution(order=None):
    report_id= "alcoholflush"
    description = _("Alcohol Flush Reaction")
    total = 0
    
    flushes_traits = UserTrait.objects.filter(report_id=report_id, value="Flushes")
    no_flushes_traits = UserTrait.objects.filter(report_id=report_id, value="Does Not Flush")
    
    
    total = flushes_traits.count() + no_flushes_traits.count()
    flushes_p = percentage(flushes_traits.count(), total)
    no_flushes_p = percentage(no_flushes_traits.count(), total)
    
    values = [{"name":_("Flushes"), "percentage":flushes_p},
              {"name": _("Does Not Flush"), "percentage":no_flushes_p}]
    if order:
        order_list(values, order)
    
    result = {"name": description, "id":0, 
            "values":values}
    return result


def get_traits_lactose_distribution(order=None):
    report_id= "lactose"
    description = _("Lactose Intolerance")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Likely Intolerant")
    b = UserTrait.objects.filter(report_id=report_id, value="Likely Tolerant")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Likely Intolerant"), "percentage":a_p},
                        {"name":_("Likely Tolerant"), "percentage":b_p}]
    
    if order:
        order_list(values, order)
                      
    return {"name": description, "id":1, 
            "values":values}
    

"""
{
            "possible_traits": [
                "If a Smoker, Likely to Smoke More",
                "Typical"
            ],
            "trait": "If a Smoker, Likely to Smoke More",
            "description": "Smoking Behavior",
            "report_id": "smokingbehavior"
        }
"""
def get_traits_smoking_distribution(order=None):
    report_id= "smokingbehavior"
    description = _("Smoking Behavior")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="If a Smoker, Likely to Smoke More")
    b = UserTrait.objects.filter(report_id=report_id, value="Typical")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Typical"), "percentage":b_p},
                      {"name":_("If a Smoker, Likely to Smoke More"), "percentage":a_p},
                        ]
    if order:
        order_list(values, order)
    return {"name": description, "id":2, 
            "values": values}


"""
        {
            "possible_traits": [
                "Can Taste",
                "Unlikely to Taste"
            ],
            "trait": "Can Taste",
            "description": "Bitter Taste Perception",
            "report_id": "bittertaste"
        },
"""
def get_traits_bitter_distribution(order=None):
    report_id= "bittertaste"
    description = _("Bitter Taste Perception")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Can Taste")
    b = UserTrait.objects.filter(report_id=report_id, value="Unlikely to Taste")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Can Taste"), "percentage":a_p},
                        {"name":_("Unlikely to Taste"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":3, 
            "values":values}
    
"""
{
            "possible_traits": [
                "Dry",
                "Wet"
            ],
            "trait": "Wet",
            "description": "Earwax Type",
            "report_id": "earwax"
        },
"""
def get_traits_earwax_distribution(order=None):
    report_id= "earwax"
    description = _("Earwax Type")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Dry")
    b = UserTrait.objects.filter(report_id=report_id, value="Wet")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Dry"), "percentage":a_p},
                        {"name":_("Wet"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":4, 
            "values":values}
    

"""
{
            "possible_traits": [
                "Likely Sprinter",
                "Unlikely Sprinter"
            ],
            "trait": "Unlikely Sprinter",
            "description": "Muscle Performance",
            "report_id": "muscleperformance"
        },
"""
def get_traits_muscleperformance_distribution(order=None):
    report_id= "muscleperformance"
    description = _("Muscle Performance")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Likely Sprinter")
    b = UserTrait.objects.filter(report_id=report_id, value="Unlikely Sprinter")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Likely Sprinter"), "percentage":a_p},
                        {"name":_("Unlikely Sprinter"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":5, 
            "values": values}


"""
        {
            "possible_traits": [
                "Likely Blue",
                "Likely Brown"
            ],
            "trait": "Likely Blue",
            "description": "Eye Color",
            "report_id": "eyecolor"
        },
"""
def get_traits_eyecolor_distribution(order=None):
    report_id= "eyecolor"
    description = _("Eye Color")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Likely Blue")
    b = UserTrait.objects.filter(report_id=report_id, value="Likely Brown")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    values = [{"name":_("Likely Blue"), "percentage":a_p},
                        {"name":_("Likely Brown"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":6, 
            "values":values}
    


"""
        {
            "possible_traits": [
                "Slightly Curlier Hair on Average",
                "Straighter Hair on Average"
            ],
            "trait": "Slightly Curlier Hair on Average",
            "description": "Hair Curl",
            "report_id": "haircurl"
        },
"""
def get_traits_haircurl_distribution(order=None):
    report_id= "haircurl"
    description = _("Hair Curl")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Slightly Curlier Hair on Average")
    b = UserTrait.objects.filter(report_id=report_id, value="Straighter Hair on Average")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Slightly Curlier Hair"), "percentage":a_p},
                        {"name":_("Straighter Hair"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":7, 
            "values":values}
    

"""
            "possible_traits": [
                "Not Resistant",
                "Possibly Resistant",
                "Resistant"
            ],
            "trait": "Not Resistant",
            "description": "Malaria Resistance (Duffy Antigen)",
            "report_id": "malariaduffy"
        },
"""
def get_traits_malariaduffy_distribution(order=None):
    report_id= "malariaduffy"
    description = _("Malaria Resistance")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Not Resistant")
    b = UserTrait.objects.filter(report_id=report_id, value="Resistant")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Not Resistant"), "percentage":a_p},
                        {"name":_("Resistant"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":8, 
            "values":values}


"""
        {
            "possible_traits": [
                "Not Resistant",
                "Resistant"
            ],
            "trait": "Not Resistant",
            "description": "Norovirus Resistance",
            "report_id": "norwalkvirus"
        },
"""
def get_traits_norwalkvirus_distribution(order=None):
    report_id= "norwalkvirus"
    description = _("Norovirus Resistance")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Not Resistant")
    b = UserTrait.objects.filter(report_id=report_id, value="Resistant")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Not Resistant"), "percentage":a_p},
                        {"name":_("Resistant"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":9, 
            "values":values} 
    

"""
        {
            "possible_traits": [
                "Not Resistant",
                "Partially Resistant"
            ],
            "trait": "Not Resistant",
            "description": "Resistance to HIV/AIDS",
            "report_id": "hiv"
        },
"""
def get_traits_hiv_distribution(order=None):
    report_id= "hiv"
    description = _("Resistance to HIV/AIDS")
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Not Resistant")
    b = UserTrait.objects.filter(report_id=report_id, value="Partially Resistant")
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    values = [{"name":_("Not Resistant"), "percentage":a_p},
                        {"name":_("Resistant"), "percentage":b_p}]
    if order:
        order_list(values, order)
    return {"name": description, "id":10, 
            "values": values} 
    
"""
{"name":_("Alcohol consumption, smoking and risk of esophageal cancer", "id":0, "values":[
                        {"name":_("Typical risk", "percentage":70},
                        {"name":_("Substantially increased risk",  "percentage":25},
                        {"name":_("Greatly increased risk", "percentage":5},]},
"""
def get_drug_alcohol_distribution():
    report_id = "alcohol_esophageal_pgx"
    description = _("Alcohol consumption, smoking and risk of esophageal cancer")
    total = 0
    
    a = UserDrugResponse.objects.filter(report_id=report_id, value="typical")
    b = UserDrugResponse.objects.filter(report_id=report_id, value="increased")
    c = UserDrugResponse.objects.filter(report_id=report_id, value="reduced")
    
    total = a.count() + b.count() + c.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    c_p = percentage(c.count(), total)
    
    return {"name":description, "id":0, "values":[
                        {"name":_("Typical risk"), "percentage":a_p},
                        {"name":_("Substantially increased risk"),  "percentage":b_p},
                        {"name":_("Reduced risk"), "percentage":c_p},]}
    

"""
{"name":_("Oral contraceptives, hormone replacement therapy and risk of venous thromboembolism", "id":1, "values":[
                        {"name":_("Normal",  "percentage":85},
                        {"name":_("Reduced",  "percentage":11},
                        {"name":_("Unable", "percentage":4}
                        
"""
def get_drug_conceptives_distribution():
    report_id = "contraceptives_vte"
    description = _("Oral contraceptives, hormone replacement therapy and risk of venous thromboembolism")
    total = 0
    
    a = UserDrugResponse.objects.filter(report_id=report_id, value="typical")
    b = UserDrugResponse.objects.filter(report_id=report_id, value="increased")
    c = UserDrugResponse.objects.filter(report_id=report_id, value="reduced")
    
    total = a.count() + b.count() + c.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    c_p = percentage(c.count(), total)
    
    return {"name":description, "id":1, "values":[
                        {"name":_("Typical risk"), "percentage":a_p},
                        {"name":_("Substantially increased risk"),  "percentage":b_p},
                        {"name":_("Reduced risk"), "percentage":c_p},]}
    

def get_global_risks():
    try:
        breastcancer = UserRisk.objects.filter(report_id="breastcancer")[0]
        celiac = UserRisk.objects.filter(report_id="celiac")[0]
        venousthromboembolism = UserRisk.objects.filter(report_id="venousthromboembolism")[0]
        melanoma = UserRisk.objects.filter(report_id="melanoma")[0]
        coronaryheartdisease = UserRisk.objects.filter(report_id="coronaryheartdisease")[0]
        lungcancer = UserRisk.objects.filter(report_id="lungcancer")[0]
        
        risks =  [
            {"name":_("Breast Cancer"), "id":0, "percentage":round(breastcancer.population_risk*100,1)},
            {"name":_("Celiac Disease"),"id":1, "percentage":round(celiac.population_risk*100,1)},
            {"name":_("Venous Thromb."), "id":2, "percentage":round(venousthromboembolism.population_risk*100,1)},
            {"name":_("Melanoma"), "id":3, "percentage":round(melanoma.population_risk*100,1)},
            {"name":_("Coronary Heart Dis."), "id":4, "percentage":round(coronaryheartdisease.population_risk*100,1)},
            {"name":_("Lung Cancer"), "id":5, "percentage":round(lungcancer.population_risk*100,1)}]
    except:
        risks =  [
            {"name":_("Breast Cancer"), "id":0, "percentage":13},
            {"name":_("Celiac Disease"),"id":1, "percentage":0.2},
            {"name":_("Venous Thromb."), "id":2, "percentage":1},
            {"name":_("Melanoma"), "id":3, "percentage":2},
            {"name":_("Coronary Heart Dis."), "id":4, "percentage":24},
            {"name":_("Lung Cancer"), "id":5, "percentage":6}]
    
    return risks
    
    