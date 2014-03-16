
import math
from utils.commons import percentage
from social_auth.models import *
from datetime import date
from users.models import Profile
from genomics.models import *
from utils.commons import percentage

def get_traits_alcohol_distribution():
    report_id= "alcoholflush"
    description = "Alcohol Flush Reaction"
    total = 0
    
    flushes_traits = UserTrait.objects.filter(report_id=report_id, value="Flushes")
    no_flushes_traits = UserTrait.objects.filter(report_id=report_id, value="Does Not Flush")
    
    
    total = flushes_traits.count() + no_flushes_traits.count()
    flushes_p = percentage(flushes_traits.count(), total)
    no_flushes_p = percentage(no_flushes_traits.count(), total)
    
    return {"name": description, "id":0, 
            "values":[{"name":"Flushes", "percentage":flushes_p},
                        {"name":"Does Not Flush", "percentage":no_flushes_p}],}


def get_traits_lactose_distribution():
    report_id= "lactose"
    description = "Lactose Intolerance"
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Likely Intolerant")
    b = UserTrait.objects.filter(report_id=report_id, value="Likely Tolerant")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    return {"name": description, "id":1, 
            "values":[{"name":"Likely Intolerant", "percentage":a_p},
                        {"name":"Likely Tolerant", "percentage":b_p}],}
    

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
def get_traits_smoking_distribution():
    report_id= "smokingbehavior"
    description = "Smoking Behavior"
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="If a Smoker, Likely to Smoke More")
    b = UserTrait.objects.filter(report_id=report_id, value="Typical")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    return {"name": description, "id":2, 
            "values":[{"name":"If a Smoker, Likely to Smoke More", "percentage":a_p},
                        {"name":"Typical", "percentage":b_p}],}


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
def get_traits_bitter_distribution():
    report_id= "bittertaste"
    description = "Bitter Taste Perception"
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Can Taste")
    b = UserTrait.objects.filter(report_id=report_id, value="Unlikely to Taste")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    return {"name": description, "id":3, 
            "values":[{"name":"Can Taste", "percentage":a_p},
                        {"name":"Unlikely to Taste", "percentage":b_p}],}
    
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
def get_traits_earwax_distribution():
    report_id= "earwax"
    description = "Earwax Type"
    total = 0
    
    a = UserTrait.objects.filter(report_id=report_id, value="Dry")
    b = UserTrait.objects.filter(report_id=report_id, value="Wet")
    
    
    total = a.count() + b.count()
    a_p = percentage(a.count(), total)
    b_p = percentage(b.count(), total)
    
    return {"name": description, "id":4, 
            "values":[{"name":"Dry", "percentage":a_p},
                        {"name":"Wet", "percentage":b_p}],}
