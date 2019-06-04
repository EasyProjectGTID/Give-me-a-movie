from django.urls import path
from recommandation.views import index, user_login, logout_user, passwordRecovery, politique
from recommandation.views import register
from django.contrib import admin as ad
from recommandation.views.cloudWordsViews import SearchCountApi, populaireTemplate, MostLikedSerie, WordOfSerie
from recommandation.views.uploadView import uploadTemplate, upload_api
from recommandation.views.views import rechercheView, similarItemsView, lastRecentView

from recommandation.views.monCompteViews import profile, ChangePassword
from recommandation.views.voteViews import vote, mesVotes, mesVotesCompute, MyUserVote
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

    path('mesvotes', mesVotes, name='mesvotes'),
    path('mesvotescompute',mesVotesCompute.as_view(), name="mesvotescompute"),
    path('MyUserVote/<pk>/', MyUserVote.as_view(), name="MyUserVote"),
    path('MyUserVote', MyUserVote.as_view(), name="MyUserVote"),


	path('populaire', populaireTemplate, name="populaire"),
    path('search-count', SearchCountApi.as_view(), name='search-count'),
    path('mostliked', MostLikedSerie.as_view(), name='mostliked'),
    path('wordof', WordOfSerie.as_view(), name='wordof'),

    path('upload', uploadTemplate, name='upload'),
    path('upload-file', upload_api, name='upload-file'),
    #Gestion du login
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('register', register, name='register'),
    path('profil', profile, name='profil'),
    path('profil/password', ChangePassword.as_view(), name='profil-password'),
    path('password', passwordRecovery, name='password'),
    path('politique', politique, name='politique'),


    #Gestion admin




]


