
from django.contrib.auth.models import User
from utils.date_util import get_days_list
from django.db.models.aggregates import Sum, Avg

def get_new_users_distribution():
    result = []
    result.append( ['Date', 'New Users'])
    day_list = get_days_list(8)
    for day in day_list:
        
        values = User.objects.filter(date_joined=day).count()
        d_index = day.strftime("%b %d")
        result.append([d_index, values])
    print result
    return result
