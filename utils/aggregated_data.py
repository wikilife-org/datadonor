# coding=utf-8

from social.models import SocialUserAggregatedData, DegreeLevel


DEFAULT_EDUCATION_LEVEL = 2

  
def complete_foursquare_info(user, foursquare_friends_count):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.foursquare_friends_count = foursquare_friends_count
    aggregated.save()
 

def get_level_of_education_by_degree(degree):
    degree, created = DegreeLevel.objects.get_or_create(title=degree)
    level = DEFAULT_EDUCATION_LEVEL
    d_level = degree.education_level()
    if degree and d_level[1] != 0:
        level = d_level[0]    
    return level


def calculate_age(born):
    today = date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
    