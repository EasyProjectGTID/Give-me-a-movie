from django.contrib import admin
from django.urls import path, include
from recommandation import urls
from recommandation.views import upload, view_serie

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('serie/', view_serie, name='serie'),

]
