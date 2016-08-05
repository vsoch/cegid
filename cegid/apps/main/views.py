from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.template import RequestContext
from django.shortcuts import render, render_to_response
import hashlib

def index_view(request):
    return render(request, 'main/index.html')

def home_view(request):
    return render(request, 'main/home.html')

def signup_view(request):
    return render(request, 'main/signup.html')

def about_view(request):
    return render(request, 'main/about.html')

def search_view(request):
    return render(request, 'main/search.html')

# Error Pages ##################################################################

def handler404(request):
    context = {"message":"Oups, we couldn't find that page!",
               "error_type":"Page Not Found"}
    response = render_to_response('main/error_base.html', context,
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    context = {"message":"Beep boop. That's a server error.",
               "error_type":"Server Error"}
    response = render_to_response('main/error_base.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
