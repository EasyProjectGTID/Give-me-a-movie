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
        print(self.request.user)
        print(self.request.data)
        serie = Series.objects.get(pk=self.request.data['args'])
        try:
            Rating.objects.create(rating=self.request.data['choice'], serie=serie, user=self.request.user)
        except:
            pass
        return HttpResponse('ok')