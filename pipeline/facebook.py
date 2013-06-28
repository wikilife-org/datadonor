
def load_data_new_user(backend, response, user, *args, **kwargs):
    if user is None:
        if backend.name == "facebook":
            try:
                url = "http://graph.facebook.com/%s/picture?width=200&height=200&redirect=false" % response['id']
                data = json.loads(urllib2.urlopen(url).read())['data']
                return {'avatar': data}
            except StandardError:
                return {'avatar': None}
        else:
            raise ValueError()
        

def get_user_avatar(backend, details, response, social_user, uid,\
                user, *args, **kwargs):
    url = None
    if getattr(backend, 'name', None) == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    if url:
        # Save the image somewhere, or just use the URL
        avatar = url
        social_user.extra_data['avatar'] = avatar
        social_user.save()
        
def load_extra_data(backend, details, response, uid, user, social_user=None,
                    *args, **kwargs):
    """Load extra data from provider and store it on current UserSocialAuth
    extra_data field.
    """
    print "TEST"
    social_user = social_user or \
                  UserSocialAuth.get_social_auth(backend.name, uid)
    if social_user:
        extra_data = backend.extra_data(user, uid, response, details)
        if kwargs.get('original_email') and not 'email' in extra_data:
            extra_data['email'] = kwargs.get('original_email')
        if extra_data and social_user.extra_data != extra_data:
            if social_user.extra_data:
                social_user.extra_data.update(extra_data)
            else:
                social_user.extra_data = extra_data
            social_user.save()
        return {'social_user': social_user}
    
def welcome_new_user(backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        Part of SOCIAL_AUTH_PIPELINE. Works with django-social-auth==0.7.21 or newer
        @backend - social_auth.backends.twitter.TwitterBackend (or other) object
        @user - User (if is_new) or django.utils.functional.SimpleLazyObject (if new_association)
        @social_user - UserSocialAuth object
    """
    if is_new:
        print "HOLa"
    else:
        print "CHAU"

    return None