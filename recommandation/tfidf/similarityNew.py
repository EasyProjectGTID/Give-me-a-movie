import operator
import time
from decimal import Decimal

import numpy
import psycopg2
import numpy as np
import math
import math
from collections import Counter
import pandas as pd
import scipy
from nltk import cluster
from scipy import spatial

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
# def cosine_distance(seriename, u, v):
#     """
#     Returns the cosine of the angle between vectors v and u. This is equal to
#     u.v / |u||v|.
#     """
#
#
#
#     return (seriename,  round(numpy.dot(u, v) / Decimal(math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))),5))

def cosine_distance(seriename, u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """

    return (seriename,  (numpy.dot(u, v)) / math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))


def buildVector(seriename, serie1, serie2):

    counter1 = serie1
    counter2 = serie2

    counter1_c = Counter()
    counter2_c = Counter()

    for k in counter1:
        counter1_c[k[0]] = k[1]
    for k in counter2:
        counter2_c[k[0]] = k[1]

    all_items = set(counter1_c.keys()).union(set(counter2_c.keys()))

    vector1 = [float(counter1_c[k]) for k in all_items]
    vector2 = [float(counter2_c[k]) for k in all_items]

    return seriename, vector1, vector2

start = time.time()
cur = conn.cursor()
cur.execute(
    "select s.id from recommandation_series s where s.name='house'")
serie_id = cur.fetchall()[0][0]

cur.execute(
    "select k.key, (p.tf * k.idf) as tfidf from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.id='{}'".format(
        serie_id))
serie_comparer = cur.fetchall()

cur.execute(
    "select s.id from recommandation_series s where s.id <> '{}'".format(serie_id))
others = cur.fetchall()
resultat = []
start = time.time()
for other in others:
    cur.execute(
        "select s.name from recommandation_series s where s.id='{}'".format(other[0]))
    seriename = cur.fetchall()[0][0]

    cur.execute(
        "select k.key, (p.tf * k.idf) as tfidf from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.id='{}'".format(
            other[0]))

    seriename, v1, v2 = buildVector(seriename, serie_comparer, cur.fetchall())

    resultat.append(cosine_distance(seriename, v1, v2))
end = time.time()
print(end-start)
print(sorted(resultat, key=operator.itemgetter(1), reverse=True))
end = time.time()
print('temps total :', end-start)