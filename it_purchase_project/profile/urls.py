from viewflow.flow.viewset import FlowViewSet
from django.conf.urls import include, url
from . import view


urlpatterns = [
url(r'^login/$', view.login, name='login'),
url(r'^logout/$', view.logout, name='logout'),]