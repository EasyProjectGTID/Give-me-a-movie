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

r = redis.Redis(host='localhost', port=6379, db=2)


def index(request):
    return render(request, 'base.html')


def recherche(request):
    """
    :param request:
    :return: utiliser pour la recherche
    """
    keywords = request.GET.get('keywords')
    resultat_json = []

    res = search(keywords)
    for serie in res[0:4]:
        serie = Series.objects.get(name=serie[0])
        resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
    return JsonResponse(resultat_json, safe=False)


def similarItems(request):
    id = request.GET.get('id')
    resultat = pickle.loads(r.get(id))
    resultat_json = []
    for pk in resultat:
        serie = Series.objects.get(id=pk[0])
        resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
    return JsonResponse(resultat_json, safe=False)


def anonymeWordCloud(request):
    resultat_json = []
    keywords = Posting.objects.filter().select_related('keywords').order_by('-number')[20:100]
    for keyword in keywords:
        resultat_json.append({'word': keyword.keywords.key, 'number': keyword.number})
    return JsonResponse(resultat_json, safe=False)


def recentItems(request):
    """Donnes les series les plus récentes"""
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

    return JsonResponse(resultat_json, safe=False)
