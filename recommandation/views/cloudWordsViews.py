import json

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from PTUT import REACT_URL, POSTER_URL
from recommandation.models import SearchCount, Rating, Series
from recommandation.views import afficheVoteFn


def populaireTemplate(request):
	user = User.objects.get(pk=request.user.pk)
	token, created = Token.objects.get_or_create(user=user)
	return render(request, 'populaire.html', {"token": token, 'base_url': REACT_URL})

class SearchCountApi(APIView):

	def get(self, *args, **kwargs):

		"""
		:param args:
		:param kwargs:
		:return:
		"""
		searchCount = SearchCount.objects.filter().order_by('-count')

		resultat_json = []
		for search in searchCount[0:20]:
			resultat_json.append({'value':search.search_key, 'count':search.count})

		return HttpResponse(json.dumps(resultat_json))


class MostLikedSerie(APIView):
	def get(self, *args, **kwargs):
		Rating.objects.filter()
		series = Series.objects.filter().annotate(vote_count=Count('rating')).order_by('-vote_count')[:10]
		resultat_json = []
		for serie in series:
			if serie.vote_count != 0:
				afficheVote = afficheVoteFn(user=self.request.user, serie=serie)
				serie.infos['Poster'] = str(POSTER_URL + str(serie.image_local))
				resultat_json.append({'value':serie.real_name, 'count': serie.vote_count,'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})

		return HttpResponse(json.dumps(resultat_json))

class WordOfSerie(APIView):
	def get(self, *args, **kwargs):

		from django.db import transaction, connection
		resultat_json = []
		with connection.cursor() as cursor:
			cursor.execute("SELECT key, tfidf from mv_{} order by tfidf DESC".format(self.request.query_params.get('id')))

			for mot in cursor.fetchall()[30:75]:
				resultat_json.append({'value':mot[0], 'count':mot[1]})


		return HttpResponse(json.dumps(resultat_json))