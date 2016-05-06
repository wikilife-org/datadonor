# coding=utf-8

from utils.user_linked_data import refresh_user_data
from django.core.management.base import BaseCommand, CommandError
from social.util.social_service_locator import SocialServiceLocator
from physical.util.physical_service_locator import PhysicalServiceLocator
from genomics.util.genomics_service_locator import GenomicsServiceLocator
from nutrition.util.nutrition_service_locator import NutritionServiceLocator
from health.util.health_service_locator import HealthServiceLocator
from social_auth.backends import SocialBackend, PhysicalBackend, GenomicsBackend, NutritionBackend, HealthBackend
from social_auth.backends import get_backends
from django.contrib.auth.models import User

import traceback
import sys



def refresh_user_physical_data(user):
    
    items = user.social_auth.all()
    key=lambda x: x
    backends = get_backends()
    for item in items:
        try:
            backend = backends[key(item.provider)]
            
                    
            if issubclass(backend, PhysicalBackend):
                service = PhysicalServiceLocator.get_instane().get_service_by_name(item.provider)
                service.pull_user_info(user.id, item.extra_data)
                
        except Exception, e:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info
            
class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            refresh_user_physical_data(user)
            
