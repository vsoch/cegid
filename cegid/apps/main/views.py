from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.template import RequestContext
from django.shortcuts import render, render_to_response
import hashlib

def index_view(request):
    context = {'active':'home'}
    return render(request, 'main/index.html', context)

def signup_view(request):
    context = {'active':'home'}
    return render(request, 'main/signup.html', context)

def about_view(request):
    context = {'active':'home'}
    return render(request, 'main/about.html', context)

def search_view(request):
    return render(request, 'main/search.html')

@requires_csrf_token
def google_auth_view(request,bid,keyid):
    '''google_auth_view generates a UID based on a gmail authentication
    :param bid: the battery id
    :param keyid: the keyid to validate the link
    '''
    battery = Battery.objects.get(id=bid)
    uid = hashlib.md5(battery.name).hexdigest()
    if uid == keyid:
        context = {"keyid":keyid,
                   "bid":bid}
        return render_to_response("main/google_auth.html",context,context_instance=RequestContext(request))
    else:
        return render_to_response("turk/robot_sorry.html")


# Error Pages ##################################################################

def handler404(request):
    response = render_to_response('main/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('main/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
