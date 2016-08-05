from django.views.generic.base import TemplateView
from django.conf.urls import patterns, url
from .views import index_view, signup_view, about_view, search_view, home_view

urlpatterns = [
    url(r'^$', index_view, name="index"),
    url(r'^search$', search_view, name="search"),
    url(r'^about$', about_view, name="about"),
    url(r'^home$', home_view, name="home")
]
