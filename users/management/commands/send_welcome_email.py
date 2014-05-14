# coding=utf-8

from utils.user_linked_data import refresh_user_data
from django.core.management.base import BaseCommand, CommandError
from users.models import Profile
from utils.commons import send_email

class Command(BaseCommand):
    def handle(self, *args, **options):
        emails = Profile.objects.filter(sent_welcome_email=False).values_list('email', flat=True).distinct()
        for email in emails:
            if email:
                #print email
                send_email(email)
                for p in Profile.objects.filter(email=email):
                    p.sent_welcome_email = True
                    p.save()
            
