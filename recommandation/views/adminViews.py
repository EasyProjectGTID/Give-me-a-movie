import datetime
import json
import pickle
import time
from _operator import itemgetter

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from recommandation.tfidf.searchTFIDF2 import search
from recommandation.models import Series, KeyWords, Posting
from django.core.cache import cache
import redis
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions


def admin(request):
    return render(request, 'admin.html')



class allSerieView(APIView):
    # permission_classes = (permissions.IsAuthenticated)
    authentication_classes = (TokenAuthentication, SessionAuthentication,)
    def get(self, *args, **kwargs):
        """
           :param request:
           :return: utiliser pour la recherche
           """
        series = Series.objects.all()
        resultat_json = []


        for serie in series:
            resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
        return HttpResponse(json.dumps(resultat_json))