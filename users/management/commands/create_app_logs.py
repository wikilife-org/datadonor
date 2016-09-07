# coding=utf-8

from utils.user_linked_data import refresh_user_data
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from physical.models import UserActivityLog
from api.models import Log, Data
from django.template.defaultfilters import slugify

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        for activity in UserActivityLog.objects.all():
            category = "Exercise"
            text = activity.type.title() if activity.type else category
            image_url = "https://s3.amazonaws.com/datadonors-app/default-exercise.jpg"
            log = Log.objects.create(user=activity.user, 
                               execute_time=activity.execute_time, 
                               text=text,
                               source=activity.provider,
                               category=category,
                               image_url=image_url)
            slug_text = slugify(text)
            if activity.miles:
                Data.objects.create(log=log, 
                                        execute_time=activity.execute_time, 
                                        log_text_slug=slug_text, 
                                        unit="miles", 
                                        value=activity.miles, 
                                        slug_unit="miles",
                                        log_category=category)
            if activity.hours:
                Data.objects.create(log=log, unit="hours", 
                                    execute_time=activity.execute_time, 
                                    log_text_slug=slug_text,
                                    value=activity.hours, slug_unit="hours",
                                    log_category=category)
            if activity.steps:
                Data.objects.create(log=log, unit="steps", 
                                    log_category=category,
                                    execute_time=activity.execute_time, 
                                    log_text_slug=slug_text,
                                    value=activity.steps, 
                                    slug_unit="steps")
        
        print "Done :)"