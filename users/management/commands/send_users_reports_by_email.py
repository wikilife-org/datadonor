# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from utils.report_users_email import  user_weekly_report

class Command(BaseCommand):
    def handle(self, *args, **options):
       user_weekly_report()
            
