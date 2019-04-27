import datetime
import json
import pickle
import time
from _operator import itemgetter

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from recommandation.tfidf.searchTFIDF2 import search
from recommandation.models import Series, KeyWords, Posting, Rating
from django.core.cache import cache
import redis
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions

r = redis.Redis(host='localhost', port=6379, db=2)


def index(request):
    if request.user.is_anonymous:
        return render(request, 'base.html')
    else:
        user = User.objects.get(pk=request.user.pk)
        token, created = Token.objects.get_or_create(user=user)
        return render(request, 'base.html', {'user': user, 'token': token})


class rechercheView(APIView):
    # permission_classes = (permissions.IsAuthenticated)
    # authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get(self, *args, **kwargs):
        """
           :param request:
           :return: utiliser pour la recherche
           """
        keywords = self.request.query_params.get('keywords')
        resultat_json = []
        if self.request.user is False:
            res = search(keywords)
            for serie in res[0:4]:
                serie = Series.objects.get(name=serie[0])
                resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
            return HttpResponse(json.dumps(resultat_json))
        else:
            res = search(keywords)
            for serie in res[0:4]:
                serie = Series.objects.get(name=serie[0])
                rating = Rating.objects.filter(user=self.request.user, serie=serie).exists()
                if rating:
                    afficheVote = False
                else:
                    afficheVote = True

                resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))



class similarItemsView(APIView):

    # permission_classes = (permissions.IsAuthenticated)
    # authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get(self, *args, **kwargs):
        if self.request.user is False:
            id = self.request.query_params.get('id')
            resultat = pickle.loads(r.get(id))
            resultat_json = []
            for pk in resultat:
                serie = Series.objects.get(id=pk[0])
                resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
            return HttpResponse(json.dumps(resultat_json))
        else:
            id = self.request.query_params.get('id')
            user = self.request.user
            resultat = pickle.loads(r.get(id))
            resultat_json = []
            for pk in resultat:

                serie = Series.objects.get(id=pk[0])

                rating = Rating.objects.filter(user=self.request.user, serie=serie).exists()
                if rating:
                    afficheVote = False
                else:
                    afficheVote = True

                resultat_json.append(
                    {'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))


class lastRecentView(APIView):
    # permission_classes = (permissions.IsAuthenticated)
    # authentication_classes = (TokenAuthentication, SessionAuthentication,)

    def get(self, *args, **kwargs):
        if self.request.user is False:
            series = Series.objects.all()
            serieToOrder = dict()
            for serie in series:
                try:
                    serieToOrder[serie] = datetime.datetime.strptime(serie.infos.get('Released', None), "%d %b %Y")
                except:
                    pass
            resultat_json = []
            for serie in sorted(serieToOrder.items(), key=itemgetter(1), reverse=True)[0:6]:
                resultat_json.append({'pk': serie[0].pk, 'name': serie[0].real_name, 'infos': serie[0].infos})
            return HttpResponse(json.dumps(resultat_json))
        else:

            series = Series.objects.all()
            serieToOrder = dict()
            for serie in series:
                try:
                    serieToOrder[serie] = datetime.datetime.strptime(serie.infos.get('Released', None), "%d %b %Y")
                except:
                    pass
            resultat_json = []
            for serie in sorted(serieToOrder.items(), key=itemgetter(1), reverse=True)[0:6]:
                print(self.request.user)
                rating = Rating.objects.filter(user=self.request.user, serie=serie[0]).exists()
                if rating:
                    afficheVote = False
                else:
                    afficheVote = True
                resultat_json.append({'pk': serie[0].pk, 'name': serie[0].real_name, 'infos': serie[0].infos, 'afficheVote': afficheVote})
        return HttpResponse(json.dumps(resultat_json))



class MyRecommandation(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    def get(self, *args, **kwargs):
            print(self.request.user)
            resultat_json = []
            ratings = Rating.objects.filter(user=self.request.user, rating='1')
            for rating in ratings:
                resultat = pickle.loads(r.get(rating.serie.pk))
                for pk in resultat:

                    serie = Series.objects.get(id=pk[0])

                    rating = Rating.objects.filter(user=self.request.user, serie=serie).exists()
                    if rating:
                        afficheVote = False
                    else:
                        afficheVote = True

                    resultat_json.append(
                        {'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))