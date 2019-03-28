from django.urls import path
from recommandation.views import index, user_login, logout_user
from recommandation.views import register

from recommandation.views.views import recherche, recentItems, similarItems, anonymeWordCloud

urlpatterns = [
    path('', index, name='index'),


    #Example
    path('recherche', recherche, name='recherche'),
    path('recent_items', recentItems, name='recent_items'),
    path('similar', similarItems, name='similarItems'),
    path('cloud', anonymeWordCloud, name='anonymeWordCloud'),

    #Gestion du login
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register, name='register'),



]


