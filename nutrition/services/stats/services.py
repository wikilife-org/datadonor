# coding=utf-8

"""
This services are used by the views
"""

from datetime import date, timedelta
from nutrition.models import *

from utils.date_util import get_days_list_int_tuple, get_days_list
from django.db.models.aggregates import Sum, Avg
from utils.commons import percentage


class NutritionDistributionService(object):

    def get_nutrients_global_distribution(self):
        nutrients = {
            "protein": {
                "title": "Protein",
                "key": "protein",
                "percentage": 0
            },
            "fat": {
                "title": "Fat",
                "key": "fat",
                "percentage": 0
            },
            "carbs": {
                "title": "Carbs",
                "key": "carbs",
                "percentage": 0
            },
            "fiber": {
                "title": "Fiber",
                "key": "fiber",
                "percentage": 0
            }
        }
        total = 0 

        from_date = date.today() - timedelta(7)            
        
        carbs_values = UserFoodLog.objects.filter(execute_time__gt=from_date).aggregate(Sum("carbs"))
        fat_values = UserFoodLog.objects.filter(execute_time__gt=from_date).aggregate(Sum("fat"))
        protein_values = UserFoodLog.objects.filter(execute_time__gt=from_date).aggregate(Sum("protein"))
        fiber_values = UserFoodLog.objects.filter(execute_time__gt=from_date).aggregate(Sum("fiber"))
        
        carb_value = carbs_values["carbs__sum"] or 0
        fat_value = fat_values["fat__sum"] or 0
        fiber_value = fiber_values["fiber__sum"] or 0
        protein_value = protein_values["protein__sum"] or 0
        
        total = carb_value + fat_value + fiber_value + protein_value
        carb_p = percentage(carb_value, total)
        fat_p = percentage(fat_value, total)
        fiber_p = percentage(fiber_value, total)
        protein_p = percentage(protein_value, total)
        
        nutrients["protein"]["percentage"] = round(protein_p)
        nutrients["carbs"]["percentage"] = round(carb_p)
        nutrients["fat"]["percentage"] = round(fat_p)
        nutrients["fiber"]["percentage"] = round(fiber_p)
        
        return nutrients
        
    def get_nutrients_user_distribution(self, user):
        nutrients = {
            "protein": {
                "title": "Protein",
                "key": "protein",
                "percentage": 0
            },
            "fat": {
                "title": "Fat",
                "key": "fat",
                "percentage": 0
            },
            "carbs": {
                "title": "Carbs",
                "key": "carbs",
                "percentage": 0
            },
            "fiber": {
                "title": "Fiber",
                "key": "fiber",
                "percentage": 0
            }
        }
        total = 0 

        from_date = date.today() - timedelta(7)
            
        carbs_values = UserFoodLog.objects.filter(user=user, execute_time__gt=from_date).aggregate(Sum("carbs"))
        fat_values = UserFoodLog.objects.filter(user=user, execute_time__gt=from_date).aggregate(Sum("fat"))
        protein_values = UserFoodLog.objects.filter(user=user, execute_time__gt=from_date).aggregate(Sum("protein"))
        fiber_values = UserFoodLog.objects.filter(user=user, execute_time__gt=from_date).aggregate(Sum("fiber"))
        
        carb_value = carbs_values["carbs__sum"] or 0
        fat_value = fat_values["fat__sum"] or 0
        fiber_value = fiber_values["fiber__sum"] or 0
        protein_value = protein_values["protein__sum"] or 0
        
        total = carb_value + fat_value + fiber_value + protein_value
        carb_p = percentage(carb_value, total)
        fat_p = percentage(fat_value, total)
        fiber_p = percentage(fiber_value, total)
        protein_p = percentage(protein_value, total)
        
        nutrients["protein"]["percentage"] = round(protein_p)
        nutrients["carbs"]["percentage"] = round(carb_p)
        nutrients["fat"]["percentage"] = round(fat_p)
        nutrients["fiber"]["percentage"] = round(fiber_p)
        
        return nutrients
 