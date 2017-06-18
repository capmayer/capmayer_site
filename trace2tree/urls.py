from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^trace/$', views.trace_view, name='trace_view'),
]
