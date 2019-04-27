import datetime
import json
import pickle
import time
from _operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
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


@login_required()
def recommandTemplate(request):
        user = User.objects.get(pk=request.user.pk)
        token, created = Token.objects.get_or_create(user=user)
        return render(request, 'base.html', {'user': user, 'token': token})
