"""
{
    u'threeCurrentPositions': {
        u'_total': 2,
        u'values': [
            {
                u'startDate': {
                    u'year': 2010,
                    u'month': 10
                },
                u'company': {
                    u'industry': u'InformationTechnologyandServices',
                    u'name': u'Wikilife'
                },
                u'id': 392487585,
                u'isCurrent': True,
                u'title': u'LeadSoftwareDeveloper'
            },
            {
                u'startDate': {
                    u'year': 2005,
                    u'month': 6
                },
                u'company': {
                    u'name': u'Sony',
                    u'ticker': u'SONY',
                    u'industry': u'InformationTechnologyandServices',
                    u'type': u'PublicCompany',
                    u'id': 1252,
                    u'size': u'10,
                    001+employees'
                },
                u'id': 21020626,
                u'isCurrent': True,
                u'title': u'AnalistaProgramadorJ2EE'
            }
        ]
    },
    u'firstName': u'L.Joaquin',
    u'headline': u'LeadSoftwareDeveloper',
    u'lastName': u'Quintas',
    u'industry': u'InformationTechnologyandServices',
    u'educations': {
        u'_total': 1,
        u'values': [
            {
                u'startDate': {
                    u'year': 2005
                },
                u'endDate': {
                    u'year': 2007
                },
                u'id': 11038212,
                u'schoolName': u'UniversidadArgentinadelaEmpresa'
            }
        ]
    },
    u'pictureUrl': u'http: //m.c.lnkd.licdn.com/mpr/mprx/0_IyKoX7is_2ZbiMandjTMX2kn_dOW3xxndgkvX2LbyooMORe9bs86EulWSTYnCZYsoxtqIwR1zzES',
    u'emailAddress': u'joako84@gmail.com',
    u'location': {
        u'name': u'Argentina'
    },
    u'threePastPositions': {
        u'_total': 2,
        u'values': [
            {
                u'startDate': {
                    u'year': 2005
                },
                u'endDate': {
                    u'year': 2007
                },
                u'title': u'JavaDeveloper',
                u'company': {
                    u'industry': u'InformationTechnologyandServices',
                    u'id': 144854,
                    u'name': u'ITResource'
                },
                u'isCurrent': False,
                u'id': 29761011
            },
            {
                u'startDate': {
                    u'year': 2004
                },
                u'endDate': {
                    u'year': 2005
                },
                u'title': u'JavaDeveloper',
                u'company': {
                    u'name': u'IBM',
                    u'ticker': u'IBM',
                    u'industry': u'InformationTechnologyandServices',
                    u'type': u'PublicCompany',
                    u'id': 1009,
                    u'size': u'10,
                    001+employees'
                },
                u'isCurrent': False,
                u'id': 62610633
            }
        ]
    },
    u'positions': {
        u'_total': 4,
        u'values': [
            {
                u'startDate': {
                    u'year': 2010,
                    u'month': 10
                },
                u'company': {
                    u'industry': u'InformationTechnologyandServices',
                    u'name': u'Wikilife'
                },
                u'id': 392487585,
                u'isCurrent': True,
                u'title': u'LeadSoftwareDeveloper'
            },
            {
                u'startDate': {
                    u'year': 2005,
                    u'month': 6
                },
                u'company': {
                    u'name': u'Sony',
                    u'ticker': u'SONY',
                    u'industry': u'InformationTechnologyandServices',
                    u'type': u'PublicCompany',
                    u'id': 1252,
                    u'size': u'10,
                    001+employees'
                },
                u'id': 21020626,
                u'isCurrent': True,
                u'title': u'AnalistaProgramadorJ2EE'
            },
            {
                u'startDate': {
                    u'year': 2005
                },
                u'endDate': {
                    u'year': 2007
                },
                u'title': u'JavaDeveloper',
                u'company': {
                    u'industry': u'InformationTechnologyandServices',
                    u'id': 144854,
                    u'name': u'ITResource'
                },
                u'isCurrent': False,
                u'id': 29761011
            },
            {
                u'startDate': {
                    u'year': 2004
                },
                u'endDate': {
                    u'year': 2005
                },
                u'title': u'JavaDeveloper',
                u'company': {
                    u'name': u'IBM',
                    u'ticker': u'IBM',
                    u'industry': u'InformationTechnologyandServices',
                    u'type': u'PublicCompany',
                    u'id': 1009,
                    u'size': u'10,
                    001+employees'
                },
                u'isCurrent': False,
                u'id': 62610633
            }
        ]
    }
}
"""
from datetime import date
import requests
from django.utils import simplejson
import oauth2 as oauth
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.aggregated_data import complete_linkedin_social_info, get_level_of_education_by_degree, complete_profile


def linkedin_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "linkedin-oauth2":
        data = kwargs.get('response')
        access_token = data["access_token"]
        
        result = get_profile( access_token)
        result["profile_img"] = result["pictureUrl"]
        del result["pictureUrl"]
        
        connections = get_connections(access_token)
        positions = get_positions(access_token)
        educations = get_educations(access_token)
        
        work_experience_years = 0
        current_year = date.today().year
        
        try:
            fist_job = positions["values"][0]
            for pos in positions["values"]:
                if fist_job["startDate"]["year"] > pos["startDate"]["year"]:
                    fist_job = pos
            
            start_year=int(fist_job["startDate"]["year"])
            work_experience_years = current_year - start_year
        except IndexError:
            pass
        
        education_level = 0
        degree = None
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
            
        linkedin_connections_count = connections["_total"]
        
        complete_linkedin_social_info(social_user.user, linkedin_connections_count, work_experience_years, education_level, degree)
        
        complete_profile(social_user.user, result["emailAddress"], None, None)
        result.update(connections)
        result.update(positions)
        result.update(educations)
        
        social_user.extra_data.update(result)
        social_user.save()
          
        return result


def get_profile( access_token, 
                params=None, headers=None):
    PROFILE_URL = "https://api.linkedin.com/v1/people/~"
    FIELDS = ":(first-name,last-name,interests,headline,industry,summary,email-address,num-connections,num-connections-capped,location:(name,country:(code)),formatted-name,following,picture-url,associations,languages,honors,educations,date-of-birth,primary-twitter-account,group-memberships,specialties,skills)"

    response = make_request('GET', PROFILE_URL+FIELDS, access_token, params=params, headers=headers)
    response = response.json()

    return response

def get_positions(access_token, params=None, headers=None):
    POSITIONS_URL = "https://api.linkedin.com/v1/people/~/positions"
    response = make_request('GET', POSITIONS_URL, access_token, params=params, headers=headers)
    response = response.json()

    return response

def get_educations(access_token, params=None, headers=None):
    EDUCATION_URL = "https://api.linkedin.com/v1/people/~/educations"
    response = make_request('GET', EDUCATION_URL, access_token, params=params, headers=headers)
    response = response.json()

    return response

def get_connections(access_token, params=None, headers=None):
    CONNECTIONS_URL = "https://api.linkedin.com/v1/people/~/connections"
    response = make_request('GET', CONNECTIONS_URL, access_token, params=params, headers=headers)
    response = response.json()

    return response

def make_request(method, url, access_token, data=None, params=None, headers=None,
                 timeout=60):
    if headers is None:
        headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
    else:
        headers.update({'x-li-format': 'json', 'Content-Type': 'application/json'})

    
    if params is None:
        params = {'oauth2_access_token': access_token}
    else:
        params['oauth2_access_token'] = access_token
    
    kw = dict(data=data, params=params,
              headers=headers, timeout=timeout)



    
    return requests.request(method.upper(), url, **kw)