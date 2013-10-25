# coding=utf-8

from wikilife.wikilife_connector import WikilifeConnector
from django.http.response import HttpResponse


#TODO add sec token
def wikilife_sync(request):
    WikilifeConnector().sync()
    return HttpResponse("ok")
