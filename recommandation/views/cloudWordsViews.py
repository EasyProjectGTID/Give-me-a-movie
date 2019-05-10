import json

from django.http import HttpResponse
from rest_framework.views import APIView

from recommandation.models import SearchCount


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
