from social_auth.backends import SocialBackend, PhysicalBackend, NutritionBackend, GenomicsBackend, HealthBackend

def association_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    request.session["association"] = Associantion()
    if isinstance(backend, SocialBackend):
        request.session["association"].type = "social"
    elif isinstance(backend, PhysicalBackend):
        request.session["association"].type = "physical"
    elif isinstance(backend, NutritionBackend):
        request.session["association"].type = "nutrition"
    elif isinstance(backend, GenomicsBackend):
        request.session["association"].type = "genomics"
    elif isinstance(backend, HealthBackend):
        request.session["association"].type = "health"

class Associantion(object):
    type = None
    
    def __init__(self, type=None):
        self.type = type