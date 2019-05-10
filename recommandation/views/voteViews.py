import datetime
import json
import locale
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
from recommandation.views import afficheVoteFn
from django.utils import formats


class vote(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get(self, *args, **kwargs):

		keywords = self.request.query_params.get('vote')
		serie = self.request.query_params.get('serie')

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
	return render(request, 'mesVotes.html', {"token": token, 'base_url': REACT_URL})


class MyUserVote(APIView):
	# permission_classes = (permissions.IsAuthenticated,)
	# authentication_classes = (TokenAuthentication,)

	def get(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return: Mes votes
		"""
		user = User.objects.get(pk=self.request.user.pk)
		token, created = Token.objects.get_or_create(user=user)
		ratings = Rating.objects.filter(user=self.request.user)
		resultat_json = []

		for rate in ratings:
			resultat_json.append({'pk': rate.serie.id, 'name': rate.serie.real_name,
								  'vote': rate.rating,
								  'date': formats.date_format(rate.date_vote, "SHORT_DATETIME_FORMAT")})

		return HttpResponse(json.dumps(resultat_json))

	def delete(self, request, pk, *args, **kwargs):
		print(pk)
		print(self.request.user)

		r = Rating.objects.filter(user=self.request.user, serie=int(pk)).delete()
		print(r)
		return HttpResponse('ok')


class mesVotesCompute(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs:
		:return: Mes recommandations en fonctions des mes votes
		"""
		ratings = Rating.objects.filter(user=self.request.user)
		like = []
		dislike = []
		resultat_json = []
		if ratings:
			for rating in ratings:
				if rating.rating == '1':
					like.append(rating.serie.id)
				if rating.rating == '0':
					dislike.append(rating.serie.id)
			resultat = compute(like=like, dislike=dislike)
			resultat_json = []
			for res in resultat[0:3]:
				serie = Series.objects.get(id=res[0])
				afficheVote = afficheVoteFn(user=self.request.user, serie=serie)
				resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})

		return HttpResponse(json.dumps(resultat_json))


