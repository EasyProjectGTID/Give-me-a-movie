import collections
import functools
import operator
import pickle
from collections import Counter

import numpy as np
import psycopg2
import redis

from PTUT import DATABASES
from recommandation.models import Series, Similarity

r = redis.Redis(host='localhost', port=6379, db=2)
conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST'],
                                                                DATABASES['default']['PASSWORD']))


# def compute(like: list, dislike: list) -> list:
# 	like_series_similar = []
# 	dislike_series_similar = []
#
# 	if len(dislike) == 0:
# 		for id in like:
# 			like_series_similar.append(dict(pickle.loads(r.get(id))))
# 		print(like_series_similar)
# 		resultat = dict(functools.reduce(operator.add, map(collections.Counter, like_series_similar)))
# 		print('1', resultat)
# 		resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))
# 		print('2', resultat)


# if len(like) == 0:
#
# 	for id in dislike:
# 		dislike_series_similar.append(dict(pickle.loads(r.get(id))))
# 	resultat = dict(functools.reduce(operator.add, map(collections.Counter, dislike_series_similar)))
# 	resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))
#
# elif len(like) != 0 and len(dislike) != 0:
#
# 	# Traitement des series que j'aime en les récuperant dans redis
# 	for id in like:
# 		like_series_similar.append(dict(pickle.loads(r.get(id))))
# 	result_i_like = dict(functools.reduce(operator.add, map(collections.Counter, like_series_similar)))
#
# 	for id in dislike:
# 		dislike_series_similar.append(dict(pickle.loads(r.get(id))))
# 	result_i_dislike = dict(functools.reduce(operator.add, map(collections.Counter, dislike_series_similar)))
# 	resultat_list = [result_i_like, result_i_dislike]
#
# 	# Resultat final
# 	resultat = functools.reduce(operator.sub, map(collections.Counter, resultat_list))
# 	resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))


# print('resultat final', resultat)
# return resultat

def compute(like: list, dislike: list) -> list:
	cur = conn.cursor()
	like_series_similar = []
	dislike_series_similar = []

	if len(dislike) == 0:
		for id in like:
			serie = Similarity.objects.filter(serie=id).order_by('-score').values_list('similar_to', 'score')
			like_series_similar.append(dict(serie))
		resultat = dict(functools.reduce(operator.add, map(collections.Counter, like_series_similar)))
		resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))


	if len(like) == 0:

		for id in dislike:
			serie = Similarity.objects.filter(serie=id).order_by('-score').values_list('similar_to', 'score')
			dislike_series_similar.append(dict(serie))
		resultat = dict(functools.reduce(operator.add, map(collections.Counter, dislike_series_similar)))
		resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))

	elif len(like) != 0 and len(dislike) != 0:


		# Traitement des series que j'aime en les récuperant dans redis
		for id in like:
			serie = Similarity.objects.filter(serie=id).order_by('-score').values_list('similar_to', 'score')
			like_series_similar.append(dict(serie))
		result_i_like = dict(functools.reduce(operator.add, map(collections.Counter, like_series_similar)))

		for id in dislike:
			serie = Similarity.objects.filter(serie=id).order_by('-score').values_list('similar_to', 'score')
			dislike_series_similar.append(dict(serie))
		result_i_dislike = dict(functools.reduce(operator.add, map(collections.Counter, dislike_series_similar)))
		resultat_list = [result_i_like, result_i_dislike]

		#Resultat final
		resultat = functools.reduce(operator.sub, map(collections.Counter, resultat_list))
		resultat = list(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))


		print('i like', result_i_like)
		print('i dislike', result_i_dislike)
	print('resultat final', resultat)
	resultat = filtering(resultat, like=like, dislike=dislike)
	print('resultat final', resultat)
	return resultat

def filtering(resultat, like=None, dislike=None):
	resultat = [x for x in resultat if x[0] not in like]
	resultat = [x for x in resultat if x[0] not in dislike]
	return resultat

# like = [16, 111, 52, 75]
# dislike = []
# compute(like=like, dislike=dislike)
