
from django.contrib.auth.models import User
from utils.date_util import get_days_list
from django.db.models.aggregates import Sum, Avg

def get_new_users_distribution():
    result = []
    
    day_list = get_days_list(8)
    for day in day_list:
        
        values = User.objects.filter(date_joined__year=day.strftime("%Y"), date_joined__month=day.strftime("%m"), date_joined__day=day.strftime("%d")).count()
        d_index = day.strftime("%b %d")
        result.append([d_index, values])
    result.reverse()
    result.insert(0, ['Date', 'New Users'])
    return result
