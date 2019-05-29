import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
import sys

from recommandation.tfidf.searchTFIDF2 import search
from recommandation.models import Series, KeyWords, Posting, Rating
from django.core.cache import cache
import redis
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions
from recommandation.tfidf.recommandationCompute import compute
from PTUT.settings import REACT_URL
from recommandation.views import afficheVoteFn


@login_required()
def recommandTemplate(request):
    user = User.objects.get(pk=request.user.pk)
    token, created = Token.objects.get_or_create(user=user)
    return render(
        request, "recommand.html", {"user": user, "token": token, "base_url": REACT_URL}
    )


class recommandView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        """

		:param args:
		:param kwargs:
		:return:
		"""

        series = Series.objects.all()
        resultat_json = []
        for serie in series:
            resultat_json.append(
                {"pk": serie.pk, "name": serie.real_name, "infos": serie.infos}
            )
        resultat_json.sort(key=lambda x: x["name"]);
        #sys.stderr.write(json.dumps(resultat_json[0]));
        return HttpResponse(json.dumps(resultat_json))

    def post(self, *args, **kwargs):
        """

		:param args:
		:param kwargs:
		:return: Donne le résultat des recommandations compute dans l'onglet recommandez moi
		"""
        print(self.request.data)
        resultat = compute(
            like=self.request.data["like"], dislike=self.request.data["dislike"]
        )
        resultat_json = []
        print(resultat)
        for res in resultat[0:3]:

            serie = Series.objects.get(id=res[0])
            afficheVote = afficheVoteFn(user=self.request.user, serie=serie)
            resultat_json.append(
                {
                    "pk": serie.pk,
                    "name": serie.real_name,
                    "infos": serie.infos,
                    "afficheVote": afficheVote,
                }
            )

        return HttpResponse(json.dumps(resultat_json))
