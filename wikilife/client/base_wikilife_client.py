# coding=utf-8

import urllib2
from urllib import urlencode


class BaseWikilifeClient(object):

    _logger = None
    _settings = None

    def __init__(self, logger, wikilife_settings):
        self._logger = logger
        self._settings = wikilife_settings

    def rest_get(self, service_path, params=None):
        """
        service_path: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url)

        return self._rest(request)

    def rest_post(self, service_path, body, params=None):
        """
        service_path: String
        body: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url, body)

        return self._rest(request)

    def rest_put(self, service_path, body, params=None):
        """
        service_path: String
        body: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url, body)
        request.get_method = lambda: 'PUT'

        return self._rest(request)

    def rest_delete(self, service_path, params=None):
        """
        service_path: String
        params: Dict<String, String>
        """
        url = self._build_url(service_path, params)
        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'

        return self._rest(request)
    
    def _build_url(self, service_path, params):
        url = self._settings["HOST"] + service_path
        if params:
            url = "%s?%s" %(url, urlencode(params))

        return url

    def _rest(self, request):
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()

        return response_code, response_headers, response_body  