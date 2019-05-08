from django.urls import path
from recommandation.views import index, user_login, logout_user
from recommandation.views import register
from django.contrib import admin as ad

from recommandation.views.views import rechercheView, similarItemsView, lastRecentView
from recommandation.views.adminViews import admin, allSerieView
from recommandation.views.monCompteViews import Profile
from recommandation.views.voteViews import vote
from recommandation.views.recommandViews import recommandTemplate, recommandView


ad.site.site_header = 'Gimme a Movie'
urlpatterns = [
    path('', index, name='index'),


    #Example
    path('recherche', rechercheView.as_view(), name='recherche'),
    path('recent_items', lastRecentView.as_view(), name='recent_items'),
    path('similar', similarItemsView.as_view(), name='similarItems'),
    path('vote', vote.as_view(), name='vote'),
    path('recommand', recommandTemplate, name='recommand'),
    path('recommand-api', recommandView.as_view(), name='recommand-api'),

    #Gestion du login
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register, name='register'),
    path('profil', Profile.as_view(), name='profile'),
    #Gestion admin
    path('administrateur', admin, name='administrateur'),
    path('all_series_admin', allSerieView.as_view(), name='all_series_admin')



]


