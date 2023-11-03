import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth

URL_GET_DEALERS = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-dealership"

def get_request(params):
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        #auth=HTTPBasicAuth('apikey', api_key))
    return response.body


def post_request(kwargs, api_key, payload):
    response = requests.post(url, params=kwargs, json=payload)
    return response.status

# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
#def get_dealers_from_cf(url, **kwargs):
def get_dealers_from_cf():
    result = get_request(url=URL_GET_DEALERS)
    return result

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


