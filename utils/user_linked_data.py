
from social.util.social_service_locator import SocialServiceLocator
from physical.util.physical_service_locator import PhysicalServiceLocator
from genomics.util.genomics_service_locator import GenomicsServiceLocator
from nutrition.util.nutrition_service_locator import NutritionServiceLocator
from social_auth.backends import SocialBackend, PhysicalBackend, GenomicsBackend, NutritionBackend, HealthBackend
from social_auth.backends import get_backends
from django.contrib.auth.models import User


def refresh_user_data(user):
    
    items = user.social_auth.all()
    key=lambda x: x
    backends = get_backends()
    for item in items:
        try:
            backend = backends[key(item.provider)]
            
            if issubclass(backend, SocialBackend):
                if item.provider != "google":
                    service = SocialServiceLocator.get_instane().build_service_by_name(item.provider)
                    service.pull_user_info(user.id, item.extra_data)
                    
            if issubclass(backend, PhysicalBackend):
                service = PhysicalServiceLocator.get_instane().get_service_by_name(item.provider)
                service.pull_user_info(user.id, item.extra_data)
                
            if issubclass(backend, GenomicsBackend):
                service = GenomicsServiceLocator.get_instane().build_service_by_name(item.provider)
                service.pull_user_info(user.id, item.extra_data)
    
            if issubclass(backend, NutritionBackend):
                service = NutritionServiceLocator.get_instane().build_service_by_name(item.provider)
                service.pull_user_info(user.id, item.extra_data)
        except:
            continue

if __name__ == '__main__':
    users = User.objects.all()
    for user in users:
        refresh_user_data(user)