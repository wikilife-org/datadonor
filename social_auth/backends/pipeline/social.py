from django.utils.translation import ugettext

from genomics.models import UserTrait, UserDrugResponse, UserRisk
from health.models import UserMoodLastWeek, UserConditions, UserComplaints, UserBloodType, UserEmotions, UserSleepLog
from nutrition.models import UserFoodLog
from physical.models import UserActivityLog
#from social.models import SocialUserAggregatedData
from users.models import Profile

from social_auth.models import UserSocialAuth, SOCIAL_AUTH_MODELS_MODULE
from social_auth.exceptions import AuthAlreadyAssociated


def social_auth_user(backend, uid, user=None, *args, **kwargs):
    """Return UserSocialAuth account for backend/uid pair or None if it
    doesn't exists.

    Merge accounts if its another login from the same user.
    
    """
    request = kwargs["request"]
    session_user = request.user
    
    social_user = UserSocialAuth.get_social_auth(backend.name, uid)
    if social_user:
        if session_user.id and social_user.user.id != session_user.id:
            change_user(social_user.user, session_user)
            social_user = UserSocialAuth.get_social_auth(backend.name, uid)
            
    return {'social_user': social_user,
            'user': social_user.user,
            'new_association': False}

def change_user(to_user, from_user):
    #Pasar las asociaciones
    for auth in UserSocialAuth.objects.filter(user=to_user):
        auth.user = from_user
        auth.save()
    
    
    #hacer merge de cuentas sociales
    #social_to_user_data = SocialUserAggregatedData.objects.get(user=to_user)
    #social_from_user_data = SocialUserAggregatedData.objects.get(user=from_user)
    social_to_user_data = to_user.social_aggregated_data
    social_from_user_data = from_user.social_aggregated_data
    
    social_from_user_data.facebook_friend_count = social_to_user_data.facebook_friend_count or social_from_user_data.facebook_friend_count
    social_from_user_data.facebook_post_weekly_avg = social_to_user_data.facebook_post_weekly_avg or social_from_user_data.facebook_post_weekly_avg
    social_from_user_data.facebook_likes_weekly_avg = social_to_user_data.facebook_likes_weekly_avg or social_from_user_data.facebook_likes_weekly_avg
    social_from_user_data.twitter_followers_count = social_to_user_data.twitter_followers_count or social_from_user_data.twitter_followers_count
    social_from_user_data.twitter_tweets_count_last_seven_days = social_to_user_data.twitter_tweets_count_last_seven_days or social_from_user_data.twitter_tweets_count_last_seven_days
    social_from_user_data.twitter_retweets_count_last_seven_days = social_to_user_data.twitter_retweets_count_last_seven_days or social_from_user_data.twitter_retweets_count_last_seven_days
    social_from_user_data.gplus_contacts_count = social_to_user_data.gplus_contacts_count or social_from_user_data.gplus_contacts_count
    social_from_user_data.linkedin_connections_count = social_to_user_data.linkedin_connections_count or social_from_user_data.linkedin_connections_count
    social_from_user_data.foursquare_friends_count = social_to_user_data.foursquare_friends_count or social_from_user_data.foursquare_friends_count
    social_from_user_data.education_level = social_to_user_data.education_level or social_from_user_data.education_level
    social_from_user_data.education_level_manual = social_to_user_data.education_level_manual or social_from_user_data.education_level_manual
    social_from_user_data.education_degree = social_to_user_data.education_degree or social_from_user_data.education_degree
    social_from_user_data.work_experience_years = social_to_user_data.work_experience_years or social_from_user_data.work_experience_years
    social_from_user_data.work_experience_years_manual = social_to_user_data.work_experience_years_manual or social_from_user_data.work_experience_years_manual
    social_to_user_data.delete()
    #eliminar registro
    #hacer merge del perfil
    profile_to_user_data = Profile.objects.get(user=to_user)
    profile_from_user_data = Profile.objects.get(user=from_user)
    profile_from_user_data.first_name = profile_to_user_data.first_name or profile_from_user_data.first_name
    profile_from_user_data.last_name = profile_to_user_data.last_name or profile_from_user_data.last_name
    profile_from_user_data.email = profile_to_user_data.last_name or profile_from_user_data.email
    profile_from_user_data.age = profile_to_user_data.age or profile_from_user_data.age
    profile_from_user_data.date_of_birth = profile_to_user_data.date_of_birth or profile_from_user_data.date_of_birth
    profile_from_user_data.gender = profile_to_user_data.gender or profile_from_user_data.gender
    profile_from_user_data.height = profile_to_user_data.height or profile_from_user_data.height
    profile_from_user_data.weight = profile_to_user_data.weight or profile_from_user_data.weight
    profile_from_user_data.device_id = profile_to_user_data.device_id or profile_from_user_data.device_id
    profile_from_user_data.timezone = profile_to_user_data.timezone or profile_from_user_data.timezone
    profile_from_user_data.city = profile_to_user_data.city or profile_from_user_data.city
    profile_from_user_data.region = profile_to_user_data.region or profile_from_user_data.region
    profile_from_user_data.country = profile_to_user_data.country or profile_from_user_data.country
    profile_from_user_data.first_name_source = profile_to_user_data.first_name_source or profile_from_user_data.first_name_source
    profile_from_user_data.last_name_source = profile_to_user_data.last_name_source or profile_from_user_data.last_name_source
    profile_from_user_data.email_source = profile_to_user_data.email_source or profile_from_user_data.email_source
    profile_from_user_data.age_source = profile_to_user_data.age_source or profile_from_user_data.age_source
    profile_from_user_data.date_of_birth_source = profile_to_user_data.date_of_birth_source or profile_from_user_data.date_of_birth_source
    profile_from_user_data.gender_source = profile_to_user_data.gender_source or profile_from_user_data.gender_source
    profile_from_user_data.height_source = profile_to_user_data.height_source or profile_from_user_data.height_source
    profile_from_user_data.weight_source = profile_to_user_data.weight_source or profile_from_user_data.weight_source
    profile_from_user_data.timezone_source = profile_to_user_data.timezone_source or profile_from_user_data.timezone_source
    profile_from_user_data.city_source = profile_to_user_data.city_source or profile_from_user_data.city_source
    profile_from_user_data.region_source = profile_to_user_data.region_source or profile_from_user_data.region_source
    profile_from_user_data.country_source = profile_to_user_data.country_source or profile_from_user_data.country_source
    profile_to_user_data.delete()
    #eliminar registro
    
    #Genomics
    for trait in UserTrait.objects.filter(user=to_user):
        trait.user = from_user
        trait.save()
    
    for drug in UserDrugResponse.objects.filter(user=to_user):
        drug.user = from_user
        drug.save()

    for risk in UserRisk.objects.filter(user=to_user):
        risk.user = from_user
        risk.save()  
    
    #Health
    #UserMoodLastWeek, UserConditions, UserComplaints, UserBloodType, UserEmotions, UserSleepLog
    to_user_mood = None
    from_user_mood = None
    try:
        to_user_mood = UserMoodLastWeek.objects.get(user=to_user)
    except:
        pass

    try:
        from_user_mood = UserMoodLastWeek.objects.get(user=from_user)
    except:
        pass
    
    if to_user_mood and from_user_mood:
        if to_user_mood.update_time > from_user_mood.update_time:
            from_user_mood.avg_mood = to_user_mood.avg_mood
            from_user_mood.save()
        to_user_mood.delete()
    elif to_user_mood and not from_user_mood:
        to_user_mood.user = from_user
        to_user_mood.save()
    
    for condition in UserConditions.objects.filter(user=to_user):
        #NO puede haber dos condiciones iguales para el mismo usuario
        from_user_condition = None
        
        try:
            if condition.type_id:
                from_user_condition = UserConditions.objects.get(user=from_user,\
                                                         condition_id = condition.condition_id,\
                                                          type_id=condition.type_id)
                    
            else:
                from_user_condition = UserConditions.objects.get(user=from_user, condition_id = condition.condition_id)

        except:
            pass
        
        if not from_user_condition:
            condition.user = from_user
            condition.save()

        condition.delete()
    
    for complaint in UserComplaints.objects.filter(user=to_user):
        #NO puede haber dos complaints iguales para el mismo usuario
        from_user_complaint = None
        
        try:
            from_user_complaint = UserComplaints.objects.get(user=from_user, complaint_id=complaint.complaint_id)
        except:
            pass
        
        if not from_user_complaint:
            complaint.user = from_user
            complaint.save()

        complaint.delete()
    
    #Emotions
    for emotion in UserEmotions.objects.filter(user=to_user):
        #NO puede haber dos emotion iguales para el mismo usuario
        from_user_emotion = None
        
        try:
            from_user_emotion = UserEmotions.objects.get(user=from_user, emotion_id=emotion.emotion_id)
        except:
            pass
        
        if not from_user_emotion:
            emotion.user = from_user
            emotion.save()

        emotion.delete()

    #Blood Type
    to_user_blood_type = None
    from_user_blood_type = None
    try:
        to_user_blood_type = UserBloodType.objects.get(user=to_user)
    except:
        pass

    try:
        from_user_blood_type = UserBloodType.objects.get(user=from_user)
    except:
        pass
    
    if to_user_blood_type and from_user_blood_type:
        if to_user_blood_type.update_time > from_user_blood_type.update_time:
            from_user_blood_type.blood_type_id = to_user_blood_type.blood_type_id
            from_user_blood_type.save()
        to_user_blood_type.delete()
    elif to_user_blood_type and not from_user_blood_type:
        to_user_blood_type.user = from_user
        to_user_blood_type.save()
    
    #UserSleepLog
    for sleep in UserSleepLog.objects.filter(user=to_user):
        sleep.user = from_user
        sleep.save()
        
    
    #Nutrition
    #UserFoodLog
    for food in UserFoodLog.objects.filter(user=to_user):
        food.user = from_user
        food.save()
        
    #Physical
    #UserActivityLog
    for activity in UserActivityLog.objects.filter(user=to_user):
        activity.user = from_user
        activity.save()
    #eliminar Usuario de Django
    to_user.delete()
    
def associate_user(backend, user, uid, social_user=None, *args, **kwargs):
    """Associate user social account with user instance."""
    if social_user or not user:
        return None

    try:
        social = UserSocialAuth.create_social_auth(user, uid, backend.name)
    except Exception, e:
        if not SOCIAL_AUTH_MODELS_MODULE.is_integrity_error(e):
            raise
        # Protect for possible race condition, those bastard with FTL
        # clicking capabilities, check issue #131:
        #   https://github.com/omab/django-social-auth/issues/131
        return social_auth_user(backend, uid, user, social_user=social_user,
                                *args, **kwargs)
    else:
        return {'social_user': social,
                'user': social.user,
                'new_association': True}


def load_extra_data(backend, details, response, uid, user, social_user=None,
                    *args, **kwargs):
    """Load extra data from provider and store it on current UserSocialAuth
    extra_data field.
    """
    social_user = social_user or \
                  UserSocialAuth.get_social_auth(backend.name, uid)
    if social_user:
        extra_data = backend.extra_data(user, uid, response, details)
        if kwargs.get('original_email') and not 'email' in extra_data:
            extra_data['email'] = kwargs.get('original_email')
        if extra_data and social_user.extra_data != extra_data:
            if social_user.extra_data:
                social_user.extra_data.update(extra_data)
            else:
                social_user.extra_data = extra_data
            social_user.save()
        return {'social_user': social_user}
