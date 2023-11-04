import requests
import json
import os
# import related models here
from . models import CarModel, CarMake, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

URL_GET_DEALERS = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-dealership"
URL_GET_REVIEWS = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-review"
URL_POST_REVIEW = "https://us-south.functions.appdomain.cloud/api/v1/web/4e4780ac-8a49-40a5-afa4-6f38d2228df1/dealership-package/get-review"
URL_WATSON_NLU_SERVICE = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1a5947e0-0f58-4ae5-b1e3-6c44df4ef4a2"
URL_ANALYZE_SENTIMENT = URL_WATSON_NLU_SERVICE + "/v1/analyze?version=2019-07-12"

#the following constant holds a name of env var which stores apikey for Watson NLU service
#you will need to setup that env var before running web server
ENV_API_KEY_WATSON_NLU = "API_KEY_WATSON_NLU"

def get_request(url, params):
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        #auth=HTTPBasicAuth('apikey', api_key))
    #print(params)
    print(f"status_code: {response.status_code}")        
    if response.status_code == 200:
        return response.json()

    return None


def post_request(url, payload):
    #print(f"url: {url}")        
    #print(f"payload: {payload}")
    if type(payload) == type("dummy"):
        raise Exception("Do not pass JSON payload as a string")

    response = requests.post(url, headers={'Content-Type': 'application/json','Content-Length': str(len(payload)), 'Accept': 'application/json'}, json=payload)
    #print(f"status_code: {response.status_code}")        
    #print(f"response: {response.json()}")        
    return response.status_code

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
                "long": d["long"], \
                "short_name": d["short_name"], \
            }
            dealer["full_name"] = d.get("full_name", "")

            #formatted_result.append(dealer)

            carDealer = CarDealer()
            carDealer.id = dealer["id"]
            carDealer.city = dealer["city"]
            carDealer.state = dealer["state"]
            carDealer.st = dealer["st"]
            carDealer.address = dealer["address"]
            carDealer.zip = dealer["zip"]
            carDealer.lat = dealer["lat"]
            carDealer.long = dealer["long"]
            carDealer.short_name = dealer["short_name"]
            carDealer.full_name = dealer["full_name"]
            formatted_result.append(carDealer)

    #print(len(result))
    return formatted_result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
#def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
#RB we do not need get_dealer_by_id_from_cf as we are reusing get_reviews to get filtered data
#def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_reviews_from_cf(params):
    result = get_request(url=URL_GET_REVIEWS, params=params)

    #print(result)
    #if we search by dealerId, then we use a different Cloudant SDK API,
    #and it returns already formatted output, so we do not need to format it
    if not(result is None) and (len(result) > 0) and (result[0].get("doc", None) == None):
        for r in result:
            analisys = analyze_review_sentiments(r["review"])
            #print(analisys)
            #print(analisys.get("sentiment",{}).get("document",{}).get("score", 0))
            #print(analisys.get("sentiment",{}).get("document",{}).get("label", 0))
            r["sentiment_score"] = analisys.get("sentiment",{}).get("document",{}).get("score", 0)
            r["sentiment_label"] = analisys.get("sentiment",{}).get("document",{}).get("label", 0)

        return result

    formatted_result = []
    for item in result:
        #print(item)
        d = item.get("doc", None)
        if (d is not None) and (d.get("id", 0) != 0):
            review = { \
                "id": d["id"], \
                "name": d["name"], \
                "dealership": d["dealership"], \
                "review": d["review"], \
                "purchase": d["purchase"], \
            }

            if (d["purchase"]):
                review["purchase_date"] = d["purchase_date"]
                review["car_make"] = d["car_make"]
                review["car_model"] = d["car_model"]
                review["car_year"] = d["car_year"]

            dealerReview = DealerReview()
            dealerReview.id = review["id"]
            dealerReview.name = review["name"]

            dealers = CarDealer.objects.filter(id=review["dealership"])
            carDealer = None
            if len(dealers) > 0:
                carDealer = dealers[0]
            else:
                #if there is no such dealer with id then create a new one
                #for referential integrity
                carDealer = CarDealer()
                carDealer.id = review["dealership"]
                #carDealer.city = ""
                #carDealer.state = ""
                #carDealer.st = dealer["st"]
                #carDealer.address = dealer["address"]
                #carDealer.zip = dealer["zip"]
                #carDealer.lat = dealer["lat"]
                #carDealer.long = dealer["long"]
                #carDealer.short_name = dealer["short_name"]
                #carDealer.full_name = dealer["full_name"]

            dealerReview.dealership = carDealer
            dealerReview.review = review["review"]
            dealerReview.purchase = review["purchase"]
            if (review["purchase"]):
                dealerReview.purchase_date = review["purchase_date"]

                #dealerReview.car_make = review["car_make"]
                makes = CarMake.objects.filter(name=review["car_make"])
                carMake = None
                if len(makes) > 0:
                    carMake = makes[0]
                else:
                    #if there is no such make with id then create a new one
                    #for referential integrity
                    carMake = CarMake()
                    carMake.name = review["car_make"]
                dealerReview.car_make = carMake

                #dealerReview.car_model = review["car_model"]
                models = CarModel.objects.filter(name=review["car_model"])
                carModel = None
                if len(models) > 0:
                    carModel = models[0]
                else:
                    #if there is no such make with id then create a new one
                    #for referential integrity
                    carModel = CarModel()
                    carModel.name = review["car_model"]
                dealerReview.car_model = carModel

                dealerReview.car_year = review["car_year"]

            formatted_result.append(review)
            
    #print(len(result))
    return formatted_result

def post_review(payload):
    result = post_request(URL_POST_REVIEW, payload)
    return result

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    # RB: instead of hardcoding apikey (which is not safe,
    # because the source code will be placed into a public repository),
    # let's put apikey into an environment variable and read it here
    apikey = os.getenv(ENV_API_KEY_WATSON_NLU)
    if (apikey is None) or (len(apikey) == 0):
        raise Exception("No apikey is set for Watson NLU service")

    payload = {"text": text, "features": {"sentiment": {}}, "language": "en"}
    header = {"Content-Type": "application/json"}
    response = requests.post(URL_ANALYZE_SENTIMENT, json=payload, headers=header, auth=HTTPBasicAuth("apikey", apikey))
    return response.json()
