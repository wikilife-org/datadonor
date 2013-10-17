# coding=utf-8

from urllib import urlencode
from wikilife_utils.parsers.json_parser import JSONParser
import urllib2


def test():
    """
    Sample Request
    
        GET /user HTTP/1.1
        Host: api.runkeeper.com
        Authorization: Bearer xxxxxxxxxxxxxxxx
        Accept: application/vnd.com.runkeeper.User+json
    
    Sample Response
    
        HTTP/1.1 200 OK
        Content-Type: application/vnd.com.runkeeper.User+json
        Content-Length: nnn
    
        {
        "userID": 1234567890,
        "profile": "/profile",
        "settings": "/settings",
        "fitness_activities": "/fitnessActivities",
        "strength_training_activities": "/strengthTrainingActivities",
        "background_activities": "/backgroundActivities",
        "sleep": "/sleep",
        "nutrition": "/nutrition",
        "weight": "/weight",
        "general_measurements": "/generalMeasurements",
        "diabetes": "/diabetes",
        "records": "/records",
        "team": "/team"
        }
    """
    access_token = "e573745473d04b3c99bce634c2349bc6"
    url = "http://api.runkeeper.com/user?access_token=%s" %access_token


    headers = {}
    headers["Authorization"] = "Bearer %s" %access_token
    headers["Accept"] = "application/vnd.com.runkeeper.User+json"

    #request = urllib2.Request(url, headers=headers)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    response_code = response.code
    response_headers = response.headers.dict
    response_body = response.read()
    response_content = JSONParser.to_collection(response_body)

    print response_code
    print response_headers
    print response_content


if __name__ == "__main__":
    test()