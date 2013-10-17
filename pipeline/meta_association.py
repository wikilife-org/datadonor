from social_auth.backends import SocialBackend, PhysicalBackend

def association_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    request.session["association"] = Associantion()
    if isinstance(backend, SocialBackend):
        request.session["association"].type = "social"


class Associantion(object):
    type = None
    
    def __init__(self, type=None):
        self.type = type