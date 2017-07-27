from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^secrets$', views.secrets),
    url(r'^post$', views.post),
    url(r'^delete$', views.delete),
    url(r'^deletea$', views.deletea),
    url(r'^like$', views.like),               
    url(r'^popular$', views.popular),
    url(r'^logout$', views.logout),
]