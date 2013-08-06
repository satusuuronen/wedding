from django.conf.urls import patterns, include, url
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from gifts.views import (LoginView, GiftView, LogoutView, GetGiftsView, BookingsView)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url('^list/$', GiftView.as_view(), name='list'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^get_gifts/(?P<pk>\d{1,1000})', BookingsView.as_view(), name='bookings'),
    url('^get_gifts/$', GetGiftsView.as_view(), name='get_gifts'),
)    

