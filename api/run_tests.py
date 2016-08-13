
import requests
import json
from datetime import datetime
from test_data import image_base64



def run_test():
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    url = "http://localhost:8080/api/log/add/"
    user_id = 1
    
    log = {"user_id":user_id, "lat":None, "lon":None, 
           "text": "Advil", "prop1_name":"cantidad", "prop1_value":2,
           "prop2_name":"intensidad", "prop2_value":3, "time": now_str}
    
    response = requests.post(url, data=json.dumps(log))
    #print response.text
    log_id = response.json()["log_id"]

    
    """image_url ="http://localhost:8080/api/log/image/add/"
    data = {"log_id":log_id, "image":image_base64}
    response = requests.post(image_url, data=json.dumps(data))
    print response.text"""
    
    
    template_url = "http://localhost:8080/api/timeline/"
    data = {"user_id":user_id}
    response = requests.get(template_url, params=data)
    print response.json()
    
    print "Get LOG"
    get_log_url = "http://localhost:8080/api/log/get/"
    data = {"user_id":user_id, "log_id":log_id}
    response = requests.get(get_log_url, params=data)
    print response.json()
    
    print "Get filter Timeline:"

    from_id = response.json()[len(response.json())-1]["log_id"]
    data = {"user_id":user_id, "from_id":from_id}
    response = requests.get(template_url, params=data)
    print response.text
    
    
    delete_log_url = "http://localhost:8080/api/log/delete/"
    data = {"user_id":user_id, "log_id":log_id}
    response = requests.post(delete_log_url, data=json.dumps(data))
    print response.text
    
    lat = "-34.5779055"
    long = "-58.4002167"
    
    print "Save log with location"
    
    url = "http://localhost:8080/api/log/add/"
    user_id = 1
    
    log = {"user_id":user_id, "lat":lat, "lon":long, 
           "text": "Advil", "prop1_name":"cantidad", "prop1_value":2,
           "prop2_name":"intensidad", "prop2_value":3, "time": now_str}
    
    response = requests.post(url, data=json.dumps(log))
    print response.text
    log_id = response.json()["log_id"]
    
    """image_url ="http://localhost:8080/api/log/image/add/"
    data = {"log_id":log_id, "image":image_base64}
    response = requests.post(image_url, data=json.dumps(data))
    print response.text"""
    
if __name__ == "__main__":
    run_test()
