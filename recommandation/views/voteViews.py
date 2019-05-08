import datetime
import json
import pickle
import time
from _operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from PTUT.settings import REACT_URL
from recommandation.tfidf.searchTFIDF2 import search
from recommandation.models import Series, KeyWords, Posting, Rating
from django.core.cache import cache
import redis
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions
from recommandation.tfidf.recommandationCompute import compute


class vote(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        """
           :param request:
           :return: utiliser pour la recherche
           """
        keywords = self.request.query_params.get('vote')
        serie = self.request.query_params.get('serie')

        print(keywords, serie)

        return HttpResponse('ok')

    def post(self, *args, **kwargs):

        serie = Series.objects.get(pk=self.request.data['args'])
        try:
            Rating.objects.create(rating=self.request.data['choice'], serie=serie, user=self.request.user)
        except Exception as e:
            print(e)
        return HttpResponse('ok')

@login_required()
def mesVotes(request):
    user = User.objects.get(pk=request.user.pk)
    token, created = Token.objects.get_or_create(user=user)
    ratings = Rating.objects.filter(user=request.user)
    like = []
    dislike = []


    return render(request, 'mesVotes.html', {'ratings':ratings, "token":token, 'base_url':REACT_URL})



class mesVotesReact(APIView):
    def get(self, *args, **kwargs):
        ratings = Rating.objects.filter(user=self.request.user)
        like = []
        dislike = []
        mesSeries = []
        if ratings:
            for rating in ratings:

                if rating.rating == '1':
                    like.append(rating.serie.id)
                if rating.rating == '0':
                    dislike.append(rating.serie.id)
            resultat = compute(like=like, dislike=dislike)
            mesSeries = []
            for res in resultat[0:3]:
                serie = Series.objects.get(name=res[0])
                rating = Rating.objects.filter(user=self.request.user, serie=serie).exists()
                if rating:
                    afficheVote = False
                else:
                    afficheVote = True
                mesSeries.append({'pk':serie.pk, 'name':serie.real_name, 'infos':serie.infos, 'afficheVote':afficheVote})

        return HttpResponse(json.dumps(mesSeries))


@login_required()
def deleteVote(request, id):
    Rating.objects.get(user=request.user, id=id).delete()
    return redirect(mesVotes)
