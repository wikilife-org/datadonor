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

def _generate_export_xls(user):

    p = user.profile
    
    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.colour_index = 2
    font0.bold = True
    
    style0 = xlwt.XFStyle()
    style0.font = font0
    
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'YYYY-MM-DD'
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Profile')
    
    ws.write(0, 0, _('First Name'), style0)
    ws.write(0, 1, _('Last Name'), style0)
    ws.write(0, 2, _('Email'), style0)
    ws.write(0, 3, _('Age'), style0)
    ws.write(0, 4, _('Date of Birth'), style0)
    ws.write(0, 5, _('Gender'), style0)
    ws.write(0, 6, _('Height'), style0)
    ws.write(0, 7, _('Weight'), style0)

    ws.write(1, 0, p.first_name, style0)
    ws.write(1, 1, p.last_name, style0)
    ws.write(1, 2, p.email, style0)
    ws.write(1, 3, p.age, style0)
    ws.write(1, 4, p.date_of_birth, style1)
    ws.write(1, 5, p.gender, style0)
    ws.write(1, 6, p.height, style0)
    ws.write(1, 7, p.weight, style0)
    
    wb.save('my_data.xls')
    return wb