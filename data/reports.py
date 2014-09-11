from physical.models import UserActivityLog
from datetime import date, datetime, time, timedelta
import time
from health.utilities import *


def _generate_export_json(user):
    
    PHYSICAL_TYPE = "physical"
    HEALTH_TYPE = "health"
    SOCIAL_TYPE = "social"
    NUTRITION_TYPE = "nutrition"
    GENOMICS_TYPE = "genomics"
    PROFILE_TYPE = "profile"
    
    export = {}    
    act_logs = UserActivityLog.objects.filter(user=user)
    for activity in act_logs:
        if activity.execute_time.strftime("%Y-%m-%d") not in export:
            export[activity.execute_time.strftime("%Y-%m-%d")] = {}
        if PHYSICAL_TYPE not in export[activity.execute_time.strftime("%Y-%m-%d")]:
            export[activity.execute_time.strftime("%Y-%m-%d")][PHYSICAL_TYPE] = []
        export[activity.execute_time.strftime("%Y-%m-%d")][PHYSICAL_TYPE].append( {"activity_type": activity.type, \
                                                                              "miles":activity.miles, "hours":activity.hours,\
                                                                               "steps": activity.steps, "source":activity.provider,\
                                                                                })
    
    conditions = user.conditions.all()
    for condition in conditions:
        if condition.update_time.strftime("%Y-%m-%d") not in export:
            export[condition.update_time.strftime("%Y-%m-%d")] = {}
        if HEALTH_TYPE not in export[condition.update_time.strftime("%Y-%m-%d")]:
            export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "conditions" not in export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["cronical_conditions"] = []
        c_name, t_name = get_conditions_name(condition.condition_id, condition.type_id)
        export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["cronical_conditions"].append({"condition_name": c_name, "condition_type":t_name, \
                                                                                                       "source":"manual_input"})
        
    
    complaints = user.complaints.all()

    for complaint in complaints:
        if complaint.update_time.strftime("%Y-%m-%d") not in export:
            export[complaint.update_time.strftime("%Y-%m-%d")] = {}
        if HEALTH_TYPE not in export[complaint.update_time.strftime("%Y-%m-%d")]:
            export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "complaints" not in export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["complaints"] = []
        
        c_name = get_complaints_name(complaint.complaint_id)
        export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["complaints"].append({"complaint_name": c_name, "source":"manual_input"})
        
    emotions = user.emotions.all()

    for emotion in emotions:
        if emotion.update_time.strftime("%Y-%m-%d") not in export:
            export[emotion.update_time.strftime("%Y-%m-%d")] = {}
        if HEALTH_TYPE not in export[emotion.update_time.strftime("%Y-%m-%d")]:
            export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "emotions" not in export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["emotions"] = []
        
        c_name = get_emotions_name(emotion.emotion_id)
        export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["emotions"].append({"emotion_name": c_name, "source":"manual_input"})

    foods = user.foods.filter()
    for food in foods:
        if food.execute_time.strftime("%Y-%m-%d") not in export:
            export[food.execute_time.strftime("%Y-%m-%d")] = {}
        if NUTRITION_TYPE not in export[food.execute_time.strftime("%Y-%m-%d")]:
            export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE] = {}
        if "nutrients" not in export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]:
            export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]["nutrients"] = []
        
        export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]["nutrients"].append({
                                                                                           "protein":food.protein, "fat":food.fat, "carbs":food.carbs,
                                                                                           "fiber":food.fiber, "source":food.provider})
    
     
    s = user.social_aggregated_data

    if s.update_time.strftime("%Y-%m-%d") not in export:
        export[p.update_time.strftime("%Y-%m-%d")] = {}
    if SOCIAL_TYPE not in export[s.update_time.strftime("%Y-%m-%d")]:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE] = {}
    
    if s.facebook_friend_count:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["facebook"] = {
                                                                            "facebook_friend_count":s.facebook_friend_count, \
                                                                            "facebook_post_weekly_avg":s.facebook_post_weekly_avg,\
                                                                            "facebook_likes_weekly_avg":s.facebook_likes_weekly_avg,
                                                                            "source":"facebook"}
    if s.twitter_followers_count:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["twitter"] = {
                                                                            "twitter_followers_count":s.twitter_followers_count, \
                                                                            "twitter_tweets_count_last_seven_days":s.twitter_tweets_count_last_seven_days,\
                                                                            "twitter_retweets_count_last_seven_days":s.twitter_retweets_count_last_seven_days,
                                                                            "source":"twitter"}
    if s.gplus_contacts_count:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["google_plus"] = {
                                                                                  "gplus_contacts_count":s.gplus_contacts_count, \
                                                                                  "source":"google_plus"} 
    
    if s.linkedin_connections_count:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["linkedin"] = {
                                                                               "linkedin_connections_count":s.linkedin_connections_count, \
                                                                               "source":"linkedin"}  
    if s.foursquare_friends_count:
        export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["foursquare"] = {
                                                                                 "foursquare_friends_count":s.foursquare_friends_count, \
                                                                                      "source":"foursquare"}         
    
    p = user.profile

    if p.update_time.strftime("%Y-%m-%d") not in export:
        export[p.update_time.strftime("%Y-%m-%d")] = {}
    if PROFILE_TYPE not in export[p.update_time.strftime("%Y-%m-%d")]:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE] = {}
    
    if p.first_name:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["first_name"] = {"value":p.first_name , "source":p.first_name_source}
    if p.last_name:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["last_name"] = {"value":p.last_name, "source":p.last_name_source}
    if p.email:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["email"] = {"value":p.email, "source":p.email_source}
    if p.age:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["age"] = {"value": p.age, "source":p.age_source}
    if p.date_of_birth:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["date_of_birth"] ={"value": p.date_of_birth.strftime("%Y-%m-%d"), "source":p.date_of_birth_source} 
    if p.gender:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["gender"] = {"value": p.gender, "source":p.gender_source}
    if p.height:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["height"] = {"value": p.height, "source":p.height_source or "manual_input"}
    if p.weight:
        export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["weight"] = {"value": p.weight, "source":p.weight_source or "manual_input"}

    return export

import xlwt
from django.utils.translation import gettext as _
from django.http.response import HttpResponse

def _generate_export_xls(user):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=my_data.xls'
    p = user.profile
    s = user.social_aggregated_data
    
    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.colour_index = 0
    font0.bold = True

    font1 = xlwt.Font()
    font1.name = 'Arial'
    font1.colour_index = 0
    font1.bold = False
    
    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'YYYY-MM-DD'

    style2 = xlwt.XFStyle()
    style2.font = font1
        
    wb = xlwt.Workbook()
    ws = wb.add_sheet('profile')
    
    ws.write(0, 0, _('first name'), style0)
    ws.write(0, 1, _('first name source'), style0)
    ws.write(0, 2, _('last name'), style0)
    ws.write(0, 3, _('last name source'), style0)
    ws.write(0, 4, _('email'), style0)
    ws.write(0, 5, _('email source'), style0)
    ws.write(0, 6, _('age'), style0)
    ws.write(0, 7, _('age source'), style0)
    ws.write(0, 8, _('date of birth'), style0)
    ws.write(0, 9, _('date of birth source'), style0)
    ws.write(0, 10, _('gender'), style0)
    ws.write(0, 11, _('gender source'), style0)
    ws.write(0, 12, _('height'), style0)
    ws.write(0, 13, _('height Unit'), style0)
    ws.write(0, 14, _('height source'), style0)
    ws.write(0, 15, _('weight'), style0)
    ws.write(0, 17, _('weight unit'), style0)
    ws.write(0, 18, _('weight source'), style0)

    ws.write(1, 0, p.first_name, style2)
    ws.write(1, 1, p.first_name_source, style2)
    ws.write(1, 2, p.last_name, style2)
    ws.write(1, 3, p.last_name_source, style2)
    ws.write(1, 4, p.email, style2)
    ws.write(1, 5, p.email_source, style2)
    ws.write(1, 6, p.age, style2)
    ws.write(1, 7, p.age_source, style2)
    ws.write(1, 8, p.date_of_birth, style1)
    ws.write(1, 9, p.date_of_birth_source, style2)
    ws.write(1, 10, p.gender, style2)
    ws.write(1, 11, p.gender_source, style2)
    ws.write(1, 12, p.height, style2)
    ws.write(1, 13, "feets", style2)
    ws.write(1, 14, p.height_source, style2)
    ws.write(1, 16, p.weight, style2)
    ws.write(1, 17, "libs", style2)
    ws.write(1, 18, p.weight_source, style2)
    
    ws_social = wb.add_sheet('social')
    ws_social.write(0, 0, _('facebook friends count'), style0)
    ws_social.write(0, 1, _('facebook post weekly avg'), style0)
    ws_social.write(0, 2, _('facebook likes weekly avg'), style0)
    ws_social.write(0, 3, _('twitter followers count'), style0)
    ws_social.write(0, 4, _('tweets count last seven days'), style0)
    ws_social.write(0, 5, _('retweets count last seven days'), style0)
    ws_social.write(0, 6, _('gplus contacts count'), style0)
    ws_social.write(0, 7, _('linkedin connections count'), style0)
    ws_social.write(0, 8, _('foursquare friends count'), style0)

    ws_social.write(1, 0, s.facebook_friend_count, style2)
    ws_social.write(1, 1, s.facebook_post_weekly_avg, style2)
    ws_social.write(1, 2, s.facebook_likes_weekly_avg, style2)
    ws_social.write(1, 3, s.twitter_followers_count, style2)
    ws_social.write(1, 4, s.twitter_tweets_count_last_seven_days, style2)
    ws_social.write(1, 5, s.twitter_retweets_count_last_seven_days, style2)
    ws_social.write(1, 6, s.gplus_contacts_count, style2)
    ws_social.write(1, 7, s.linkedin_connections_count, style2)
    ws_social.write(1, 8, s.foursquare_friends_count, style2)
    
    ws_nutrition = wb.add_sheet('nutrition')
    ws_nutrition.write(0, 0, _('date'), style0)
    ws_nutrition.write(0, 1, _('protein'), style0)
    ws_nutrition.write(0, 2, _('fat'), style0)
    ws_nutrition.write(0, 3, _('carbs'), style0)
    ws_nutrition.write(0, 4, _('fiber'), style0)
    ws_nutrition.write(0, 5, _('source'), style0)

    foods = user.foods.all()
    food_index = 0
    for food in foods:
        ws_nutrition.write(food_index, 0,food.execute_time, style1)
        ws_nutrition.write(food_index, 1,food.protein, style0)
        ws_nutrition.write(food_index, 2, food.fat, style0)
        ws_nutrition.write(food_index, 3, food.carbs, style0)
        ws_nutrition.write(food_index, 4, food.fiber, style0)
        ws_nutrition.write(food_index, 5, food.provider, style0)
        food_index = food_index + 1


    ws_emotions = wb.add_sheet('emotions')
    ws_emotions.write(0, 0, _('date'), style0)
    ws_emotions.write(0, 1, _('name'), style0)
    ws_emotions.write(0, 2, _('source'), style0)

    emotions = user.emotions.all()
    emotions_index = 0
    for emotion in emotions:
        ws_emotions.write(emotions_index, 0, emotion.update_time, style1)
        ws_emotions.write(emotions_index, 1, get_emotions_name(emotion.emotion_id), style0)
        ws_emotions.write(emotions_index, 2, "manual_input", style0)

        emotions_index = emotions_index + 1

    ws_complaints = wb.add_sheet('complaints')
    ws_complaints.write(0, 0, _('date'), style0)
    ws_complaints.write(0, 1, _('name'), style0)
    ws_complaints.write(0, 2, _('source'), style0)

    complaints = user.complaints.all()
    complaints_index = 0
    for complaint in complaints:
        ws_complaints.write(complaints_index, 0, complaint.update_time, style1)
        ws_complaints.write(complaints_index, 1, get_complaints_name(complaint.complaint_id), style0)
        ws_complaints.write(complaints_index, 2, "manual_input", style0)

        complaints_index = complaints_index + 1

    ws_conditions = wb.add_sheet('conditions')
    ws_conditions.write(0, 0, _('date'), style0)
    ws_conditions.write(0, 1, _('name'), style0)
    ws_conditions.write(0, 2, _('source'), style0)

    conditions = user.conditions.all()
    conditions_index = 0
    for condition in conditions:
        ws_conditions.write(conditions_index, 0, condition.update_time, style1)
        ws_conditions.write(conditions_index, 1, get_conditions_name(condition.condition_id), style0)
        ws_conditions.write(conditions_index, 2, "manual_input", style0)

        conditions_index = conditions_index + 1
        

    ws_physical = wb.add_sheet('physical')
    ws_physical.write(0, 0, _('date'), style0)
    ws_physical.write(0, 1, _('activity name'), style0)
    ws_physical.write(0, 2, _('miles'), style0)
    ws_physical.write(0, 3, _('minutes'), style0)
    ws_physical.write(0, 4, _('steps'), style0)
    ws_physical.write(0, 5, _('source'), style0)

    act_logs = UserActivityLog.objects.filter(user=user)
    act_index = 0
    for log in act_logs:
        ws_physical.write(act_index, 0,log.execute_time, style1)
        ws_physical.write(act_index, 1,log.type, style0)
        ws_physical.write(act_index, 2, log.miles, style0)
        ws_physical.write(act_index, 3, log.hours * 60, style0)
        ws_physical.write(act_index, 4, log.steps, style0)
        ws_physical.write(act_index, 5, log.provider, style0)
        act_index = act_index + 1
    

    wb.save(response)
    return response