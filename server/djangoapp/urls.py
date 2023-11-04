from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path(route='registration_request', view=views.registration_request, name='registration_request'),

    # path for login
    path(route='login_request', view=views.login_request, name='login_request'),

    # path for logout
    path(route='logout_request', view=views.logout_request, name='logout_request'),

    # landing page
    #path(route='', view=views.get_dealerships, name='index'),
    path(route='', view=views.get_dealerships, name='get_dealerships'),

    #extra pages
    path(route='dealer_details/<int:dealerId>', view=views.dealer_details, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),

    #back-end API calls
    path(route='api/dealership', view=views.api_get_dealerships, name='api_get_dealerships'),
    path(route='api/review', view=views.api_get_reviews),
    path(route='api/sentiment_analysis', view=views.sentiment_analysis),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)