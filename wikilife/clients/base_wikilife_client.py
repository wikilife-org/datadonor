# coding=utf-8

from urllib import urlencode
from wikilife_utils.parsers.json_parser import JSONParser
import urllib2
import requests


class BaseWikilifeClient(object):

    _settings = None

    def __init__(self, wikilife_settings):
        self._settings = wikilife_settings

    def rest_get(self, service_path, params=None, response_to_json=True):
        """
        service_path: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url)

        return self._rest(request, response_to_json)

    def rest_post(self, service_path, request_dto, params=None, response_to_json=True):
        """
        service_path: String
        request_dto: dict
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request_body = JSONParser.to_json(request_dto)
        r = requests.post(url, data=request_body)
        return r.json()
        #request = urllib2.Request(url, request_body)

        #return self._rest(request, response_to_json)

    def rest_put(self, service_path, request_dto, params=None, response_to_json=True):
        """
        service_path: String
        request_dto: dict
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request_body = JSONParser.to_json(request_dto)
        request = urllib2.Request(url, request_body)
        request.get_method = lambda: 'PUT'

        return self._rest(request, response_to_json)

    def rest_delete(self, service_path, params=None, response_to_json=True):
        """
        service_path: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'

        return self._rest(request, response_to_json)

    def _build_url(self, service_path, params):
        url = self._settings["HOST"] + service_path
        if params:
            url = "%s?%s" %(url, urlencode(params))

        return url

    def _rest(self, request, response_to_json=True):
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()

        if response_to_json:
            response_content = JSONParser.to_collection(response_body)
        else:
            response_content = response_body

        return response_code, response_headers, response_content