# coding=utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from social_auth.utils import setting
from utils.email import EMail


def percentage(value, total):
    if total == 0:
        return 0
    return (value * 100) /float(total)


def send_email(to_email):

    #plaintext = get_template('email/welcome.txt')
    #htmly     = get_template('email/welcome.html')
    
    d = Context({})
    
    subject = 'Welcome to Datadonors!'
    from_email = setting("WELCOME_EMAIL_FROM", "no-reply@wikilife.org")
    #text_content = plaintext.render(d)
    #html_content = htmly.render(d)
    msg = EMail( [to_email], subject)
    msg.html("email/welcome.html", d)
    msg.text("email/welcome.txt", d)
    #msg.attach_alternative(html_content, "text/html")
    msg.send(from_email)

def send_email_report(to_email, subject, context):
    """
    Report Emails to users sender
    """
    d = Context(context)
    from_email = setting("WELCOME_EMAIL_FROM", "no-reply@wikilife.org")
    msg = EMail( [to_email], subject)
    msg.html("email/report.html", d)
    msg.text("email/report.txt", d)
    msg.send(from_email)
    
def send_email_internal_report(to_email, report):

    #plaintext = get_template('email/welcome.txt')
    #htmly     = get_template('email/welcome.html')
    
    d = Context({"result":report})
    
    subject = 'Datadonors: Daily Report'
    from_email = setting("WELCOME_EMAIL_FROM", "no-reply@wikilife.org")
    #text_content = plaintext.render(d)
    #html_content = htmly.render(d)
    msg = EMail( [to_email], subject)
    msg.html("email/new_users_report.html", d)
    msg.text("email/new_users_report.txt", d)
    #msg.attach_alternative(html_content, "text/html")
    msg.send(from_email)
    
DEFAULT_EDUCATION_LEVEL = 2


def get_level_of_education_by_degree(degree):
    from social.models import DegreeLevel
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


from django.contrib.auth.models import User
from physical.models import UserActivityLog
from datetime import date, datetime, time, timedelta
import time

def last_week_user_actions(user):
    ctx = {"show_social":True}
    
    today = date.today()
    last_sunday = today - timedelta(days=6)
    
    act_logs = UserActivityLog.objects.filter(execute_time__range=(last_sunday, today), \
                                           type__in=["walking", "running", "cycling"], user=user)
    
    if len(act_logs) > 0:
        ctx["show_physical"] = True
    else:
        ctx["show_physical"] = False
        
    
    if len(user.conditions.all()) > 0 or len(user.complaints.all()) or len(user.emotions.all()) > 0 :
        ctx["show_health"] = True
    else:
        ctx["show_health"] = False
    
    if len(user.foods.filter(execute_time__range=(last_sunday, today))) > 0:
        ctx["show_nutrition"] = True
    else:
        ctx["show_nutrition"] = False

    if len(user.traits.all()) > 0 or len(user.drug_reponse.all()) or len(user.risks.all()) > 0 :
        ctx["show_genomics"] = True
    else:
        ctx["show_genomics"] = False
      
    
    return ctx
                                           
    