# coding=utf-8

from django.core.management.base import BaseCommand, CommandError
from utils.report_physical_email import  physical_weekly_report

class Command(BaseCommand):
    def handle(self, *args, **options):
       physical_weekly_report()
            
