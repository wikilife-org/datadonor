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