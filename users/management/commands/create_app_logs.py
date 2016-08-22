# coding=utf-8

from utils.user_linked_data import refresh_user_data
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from physical.models import UserActivityLog
from api.models import Log, Data


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
            if activity.miles:
                Data.objects.create(log=log, unit="miles", value=activity.miles, slug_unit="miles")
            if activity.hours:
                Data.objects.create(log=log, unit="hours", value=activity.hours, slug_unit="hours")
            if activity.steps:
                Data.objects.create(log=log, unit="steps", value=activity.steps, slug_unit="steps")
        
        print "Done :)"