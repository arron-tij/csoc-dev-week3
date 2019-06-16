from django.urls import path
from authentication import views as core_views
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^signup/$', core_views.signup, name='signup'), 
]