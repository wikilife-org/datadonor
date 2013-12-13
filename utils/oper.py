
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
    
    
