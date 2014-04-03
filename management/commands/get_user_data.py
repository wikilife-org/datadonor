# coding=utf-8

from utils.user_linked_data import refresh_user_data
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            refresh_user_data(user)
            
