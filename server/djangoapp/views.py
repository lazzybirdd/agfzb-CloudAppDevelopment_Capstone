from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from . import restapis
from . models import CarModel, CarMake, CarDealer, DealerReview

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealership_list = api_get_dealerships(request)
    context["dealership_list"] = dealership_list

    print(len(dealership_list))
    print(type(dealership_list[0]))
    print(dealership_list[0].short_name)

    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

def api_get_dealerships(request):
    if request.method == "GET":
        params = {"state": request.GET.get("state", default="")}
        result = restapis.get_dealers_from_cf(params)
        #return HttpResponse(result, content_type="application/json")
        return result

    return []

def api_get_reviews(request):
    if request.method == "GET":
        params = {"dealerId": request.GET.get("dealerId", default="")}
        result = restapis.get_dealer_reviews_from_cf(params)
        return HttpResponse(str(result), content_type="application/json")

    if request.method == "POST":
        result = restapis.post_review(params, request.text)
        return HttpResponse(str(result), content_type="application/json")

    return []

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    result = restapis.get_dealer_reviews_from_cf ({"dealerId": dealer_id})
    return HttpResponse(str(result), content_type="application/json")

# Create a `get_dealer_details` view to render the reviews of a dealer
def dealer_details(request, dealerId):
    context={}
    print(f"dealerId={dealerId}")
    result = restapis.get_dealer_reviews_from_cf({"dealerId": dealerId})
    #return HttpResponse(str(result), content_type="application/json")

    print(f"reviews count: {len(result)}")
    #print(result)
    context["review_list"] = result

    dealers = CarDealer.objects.filter(id=dealerId)
    print(f"dealers count: {len(dealers)}")
    if len(dealers) == 0:
        allDealers = restapis.get_dealers_from_cf({})
        dealers = [ x for x in allDealers if str(x.id) == str(dealerId)]

    print(f"updated dealers count: {len(dealers)}")
    context["dealer"] = dealers[0]
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    result = restapis.post_review({"dealerId": dealer_id}, request.text)
    return HttpResponse(str(result), content_type="application/json")

def sentiment_analysis(request):
    result = restapis.analyze_review_sentiments(request.GET.get("text", default=""))
    return HttpResponse(str(result), content_type="application/json")
