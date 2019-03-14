from django.urls import path
from recommandation.views import index, user_login, logout_user
from recommandation.views import register

from recommandation.views.views import recherche, recommandation_anonyme, similarItems

urlpatterns = [
    path('', index, name='index'),


    #Example
    path('recherche', recherche, name='recherche'),
    path('recommandation_anonyme', recommandation_anonyme, name='recommandation_anoynme'),
    path('similar', similarItems, name='similarItems'),

    #Gestion du login
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register, name='register'),



]


