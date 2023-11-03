import requests
import json
# import related models here
from . models import *
from requests.auth import HTTPBasicAuth

URL_GET_DEALERS = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-dealership"
URL_GET_REVIEWS = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-review"

def get_request(url, params):
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        #auth=HTTPBasicAuth('apikey', api_key))
    print(params)
    print(response.status_code)        
    if response.status_code == 200:
        return response.json()

    return None


def post_request(url, params, payload):
    response = requests.post(url, params=params, json=payload)
    return response.status

# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
#def get_dealers_from_cf(url, **kwargs):
def get_dealers_from_cf(params):
    result = get_request(url=URL_GET_DEALERS, params=params)

    #print(result)

    #if we search by state, then we use a different Cloudant SDK API,
    #and it returns already formatted output, so we do not need to format it
    if (len(result) > 0) and (result[0].get("doc", None) == None):
        return result

    formatted_result = []
    for item in result:
        #print(item)
        d = item.get("doc", None)
        if (d is not None) and (d.get("id", 0) != 0):
            dealer = { \
                "id": d["id"], \
                "city": d["city"], \
                "state": d["state"], \
                "st": d["st"], \
                "address": d["address"], \
                "zip": d["zip"], \
                "lat": d["lat"], \
                "long": d["long"] \
            }
            formatted_result.append(dealer)

            carDealer = CarDealer()
            carDealer.id = dealer["id"]
            carDealer.city = dealer["city"]
            carDealer.state = dealer["state"]
            carDealer.st = dealer["st"]
            carDealer.address = dealer["address"]
            carDealer.zip = dealer["zip"]
            carDealer.lat = dealer["lat"]
            carDealer.long = dealer["long"]

            #formatted_result.append(carDealer)
    #print(len(result))
    return formatted_result

def get_reviews(params):
    result = get_request(url=URL_GET_REVIEWS, params=params)

    #print(result)

    formatted_result = []
    for item in result:
        print(item)
        d = item.get("doc", None)
        if (d is not None) and (d.get("id", 0) != 0):
            dealer = { \
                "id": d["id"], \
                "name": d["name"], \
                "dealership": d["dealership"], \
                "review": d["review"], \
                "purchase": d["purchase"], \
            }

            if (dealer["purchase"]):
                d["purchase_date"] = d["purchase_date"]
                d["car_make"] = d["car_make"]
                d["car_model"] = d["car_model"]
                d["car_year"] = d["car_year"]

            formatted_result.append(dealer)
    #print(len(result))
    return formatted_result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    pass

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    pass


