import requests
import time

def treshold_endpoint_get_request(endpoint) :
    result=requests.get(endpoint)
    if result.status_code==429 or result.status_code==503: 
            while result.status_code==429 or result.status_code==503:
                print("Rate limit reached.Waiting 11 secs...")
                time.sleep(11)
                result=requests.get(endpoint)
            return result
    return result
