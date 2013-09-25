"""
Runkeeper
"""

def runkeeper_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "runkeeper":
        data = kwargs.get('response')
        print data