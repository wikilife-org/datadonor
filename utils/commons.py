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


def send_email(to_email, template_html, template_txt):

    plaintext = get_template('email/welcome.txt')
    htmly     = get_template('email/welcome.html')
    
    d = Context({})
    
    subject = 'Welcome to Datadonors!'
    from_email = setting("WELCOME_EMAIL_FROM", "no-reply@wikilife.org")
#    text_content = plaintext.render(d)
#    html_content = htmly.render(d)
    msg = EMail( [to_email], subject)
    msg.html("email/welcome.html", d)
    msg.text("email/welcome.txt", d)
 #   msg.attach_alternative(html_content, "text/html")
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
    