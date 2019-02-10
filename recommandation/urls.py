from django.urls import path
from recommandation.views import index, user_login, logout_user
from recommandation.views.series import listeSeries, detailSerie
from recommandation.utils.getSerieInfo import getInfos
from recommandation.views.index import recherche
urlpatterns = [
    path('', index, name='index'),
    path('listeDesSeries', listeSeries, name='listeSeriesNomURL'),
    path('detail/serie/<id>/', detailSerie, name='detailSerie'),

    #Example
    path('recherche', recherche, name='recherche'),

    #Gestion du login
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),



]


