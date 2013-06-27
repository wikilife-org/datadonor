
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