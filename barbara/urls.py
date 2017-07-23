from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^comeco/$', views.view_init, name='view_init'),
]
