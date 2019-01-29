from django.contrib import admin
from django.urls import path, include
from recommandation import urls
from recommandation.views import index, listeSeries, detailSerie

urlpatterns = [
    path('', index, name='index'),
    path('listeDesSeries', listeSeries, name='listeSeriesNomURL'),
    path('detailSerie/<id>/', detailSerie, name='detailSerie')


]
