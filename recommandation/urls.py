from django.contrib import admin
from django.urls import path, include
from recommandation import urls
from recommandation.views import index

urlpatterns = [
    path('', index, name='index'),


]
