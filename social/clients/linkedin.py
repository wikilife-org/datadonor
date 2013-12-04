# coding=utf-8

from datetime import date
import requests
from utils.aggregated_data import get_level_of_education_by_degree
from social.clients.base_device_client import BaseDeviceClient


class LinkedinClient(BaseDeviceClient):

    _api_host = None
    _access_token = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token

    def get_profile(self, params=None, headers=None):
        PROFILE_URL = "people/~"
        FIELDS = ":(first-name,last-name,interests,headline,industry,summary,email-address,num-connections,num-connections-capped,location:(name,country:(code)),formatted-name,following,picture-url,associations,languages,honors,educations,date-of-birth,primary-twitter-account,group-memberships,specialties,skills)"
        response = self.make_request('GET', PROFILE_URL+FIELDS, params=params, headers=headers)
        response = response.json()
        return response

    def get_positions(self, params=None, headers=None):
        POSITIONS_URL = "people/~/positions"
        response = self.make_request('GET', POSITIONS_URL, params=params, headers=headers)
        response = response.json()
        return response
    
    def get_educations(self, params=None, headers=None):
        EDUCATION_URL = "people/~/educations"
        response = self.make_request('GET', EDUCATION_URL, params=params, headers=headers)
        response = response.json()
        return response
    
    def get_connections(self, params=None, headers=None):
        CONNECTIONS_URL = "people/~/connections"
        response = self.make_request('GET', CONNECTIONS_URL, params=params, headers=headers)
        response = response.json()
        return response
    
    def get_work_experience_years(self):
        work_experience_years = 0
        current_year = date.today().year
        positions = self.get_positions()
        
        try:
            fist_job = positions["values"][0]
            for pos in positions["values"]:
                if fist_job["startDate"]["year"] > pos["startDate"]["year"]:
                    fist_job = pos
            
            start_year=int(fist_job["startDate"]["year"])
            work_experience_years = current_year - start_year
        except IndexError:
            pass
        except KeyError:
            #Que hacemos si no tiene startDate
            pass
        return work_experience_years

    
    def get_education_level(self):
        education_level = 2
        degree = None
        educations = self.get_educations()
        try:
            education_degree = educations["values"][0]
            for edu in educations["values"]:
                if education_degree["endDate"]["year"] < edu["endDate"]["year"]:
                    education_degree = edu
            
            
            if "degree" in education_degree:
                degree = education_degree["degree"]
                education_level = get_level_of_education_by_degree(degree)
        except IndexError:
            pass
        except KeyError:
            #Que hacemos si no tiene endDate
            pass
        return education_level, degree

    def get_connections_count(self):
        return int(self.get_connections()["_total"])

    def make_request(self, method, url, data=None, params=None, headers=None, timeout=60):
        if headers is None:
            headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
        else:
            headers.update({'x-li-format': 'json', 'Content-Type': 'application/json'})
            
        if params is None:
            params = {'oauth2_access_token': self._access_token}
        else:
            params['oauth2_access_token'] = self._access_token
        
        kw = dict(data=data, params=params, headers=headers, timeout=timeout)
        request_url = self._api_host + url
        
        return requests.request(method.upper(), request_url, **kw)