from django.contrib.auth import REDIRECT_FIELD_NAME

from social_auth.models import UserSocialAuth
from social_auth.backends import get_backends
from social_auth.utils import group_backend_by_type, LazyDict

# Note: social_auth_backends, social_auth_by_type_backends and
#       social_auth_by_name_backends don't play nice together.


def social_auth_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key.
    """
    def context_value():
        return backends_data(request.user)
    return {'social_auth': LazyDict(context_value)}


def social_auth_by_type_backends(request):
    """Load Social Auth current user data to context.
    Will add a output from backends_data to context under social_auth key where
    each entry will be grouped by backend type (openid, oauth, oauth2).
    """
    def context_value():
        data = backends_data(request.user)
        data['backends'] = group_backend_by_type(data['backends'])
        data['not_associated'] = group_backend_by_type(data['not_associated'])
        data['associated'] = group_backend_by_type(
            data['associated'],
            key=lambda assoc: assoc.provider
        )
        return data
    return {'social_auth': LazyDict(context_value)}


def social_auth_by_name_backends(request):
    """Load Social Auth current user data to context.
    Will add a social_auth object whose attribute names are the names of each
    provider, e.g. social_auth.facebook would be the facebook association or
    None, depending on the logged in user's current associations. Providers
    with a hyphen have the hyphen replaced with an underscore, e.g.
    google-oauth2 becomes google_oauth2 when referenced in templates.
    """
    def context_value():
        keys = get_backends().keys()
        accounts = dict(zip(keys, [None] * len(keys)))
        user = request.user
        if hasattr(user, 'is_authenticated') and user.is_authenticated():
            accounts.update((assoc.provider.replace('-', '_'), assoc)
                    for assoc in UserSocialAuth.get_social_auth_for_user(user))
        return accounts
        print accounts
    return {'social_auth': LazyDict(context_value)}


def backends_data(user):
    """Return backends data for given user.

    Will return a dict with values:
        associated: UserSocialAuth model instances for currently
                    associated accounts
        not_associated: Not associated (yet) backend names.
        backends: All backend names.

    If user is not authenticated, then first list is empty, and there's no
    difference between the second and third lists.
    """
    available = get_backends().keys()
    values = {"social": {'associated': [], 'not_associated':available},
              "physical": {'associated': [], 'not_associated':available},
              "nutrition": {'associated': [], 'not_associated':available},
              "health": {'associated': [], 'not_associated':available},
              "genomics": {'associated': [], 'not_associated':available},
              'associated': [],
              'not_associated': available,
              'backends': available}
    # Beware of cyclical imports!
    key=lambda x: x
    from social_auth.backends import SocialBackend, PhysicalBackend, GenomicsBackend, NutritionBackend, HealthBackend
    # user comes from request.user usually, on /admin/ it will be an instance
    # of auth.User and this code will fail if a custom User model was defined
    if hasattr(user, 'is_authenticated') and user.is_authenticated():
        associated = UserSocialAuth.get_social_auth_for_user(user)
        not_associated = list(set(available) -
                              set(assoc.provider for assoc in associated))
        
        
        backends = get_backends()
        not_associated_s = []
        not_associated_p = []
        not_associated_g = []
        not_associated_h = []
        not_associated_n = []
        
        for item in associated:
            backend = backends[key(item.provider)]
            if issubclass(backend, SocialBackend):
                values['social']["associated"].append(item.provider)
            if issubclass(backend, PhysicalBackend):
                values["physical"]["associated"].append(item.provider)
            if issubclass(backend, GenomicsBackend):
                values["genomics"]["associated"].append(item.provider)
            if issubclass(backend, NutritionBackend):
                values["nutrition"]["associated"].append(item.provider)
            if issubclass(backend, HealthBackend):
                values["health"]["associated"].append(item.provider)
        for item in not_associated:
            backend = backends[key(item)]
            if issubclass(backend, SocialBackend):
                not_associated_s.append(item)
            if issubclass(backend, PhysicalBackend):
                not_associated_p.append(item)
            if issubclass(backend, GenomicsBackend):
                not_associated_g.append(item)
            if issubclass(backend, NutritionBackend):
                not_associated_n.append(item)
            if issubclass(backend, HealthBackend):
                not_associated_h.append(item)
        
        values['social']["not_associated"] = not_associated_s
        values['physical']["not_associated"] = not_associated_p
        values['genomics']["not_associated"] = not_associated_g
        values['nutrition']["not_associated"] = not_associated_n
        values['health']["not_associated"] = not_associated_h
        values['associated'] = associated
        values['not_associated'] = not_associated
    return values


def social_auth_login_redirect(request):
    """Load current redirect to context."""
    redirect_value = request.REQUEST.get(REDIRECT_FIELD_NAME)
    if redirect_value:
        redirect_querystring = REDIRECT_FIELD_NAME + '=' + redirect_value
    else:
        redirect_querystring = ''

    return {
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
        'REDIRECT_FIELD_VALUE': redirect_value,
        'redirect_querystring': redirect_querystring
    }
