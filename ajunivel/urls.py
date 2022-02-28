# -*- coding: utf-8 -*-
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('ajunivel', views.index, name='index'),
    path('menu', views.menu, name='menu'),
]