from django.views.generic.base import TemplateView
from django.conf.urls import patterns, url
from .views import index_view, signup_view, about_view, search_view, google_auth_view

urlpatterns = patterns('',
    url(r'^$', index_view, name="index"),
    url(r'^search$', search_view, name="search"),
    url(r'^batteries/(?P<bid>\d+|[A-Z]{8})/(?P<keyid>\d+|[A-Za-z0-9-]{32})/auth$',google_auth_view,name='google_auth_view'), # use google for auth
    url(r'^about$', about_view, name="about")
)
