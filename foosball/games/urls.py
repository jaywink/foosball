# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GameListView.as_view(), name="index"),
    url(r'^detail/(?P<pk>\d+)/$', views.GameDetailView.as_view(), name="detail"),
    url(r'^new/$', views.GameCreateView.as_view(), name="new"),
]
