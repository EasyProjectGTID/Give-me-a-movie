import operator
import time
from decimal import Decimal

import psycopg2
import numpy
import math
import math
from collections import Counter

import redis
from nltk import cluster

#r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
from PTUT import DATABASES

conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST'],
                                                                DATABASES['default']['PASSWORD']))




def cosine_distance(seriename, u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """

    return (seriename, (numpy.dot(u, v)) / math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))


def buildVector(seriename, serie1, serie2):

    counter1 = serie1
    counter2 = serie2

    counter1_c = Counter()
    counter2_c = Counter()
    s1 = time.time()
    for k in counter1:
        counter1_c[k[0]] = k[1]
    for k in counter2:
        counter2_c[k[0]] = k[1]
    #retranscrit tableau contenant id_keword-tfidf  en counter pour les memes données

    s1e = time.time()
    print('s1', s1e -s1)

    s2 = time.time()
    all_items = set(counter1_c.keys()).union(set(counter2_c.keys()))
    #all_items= les clés des keywords pour les deux séries en 1 fois
    s2e = time.time()
    print('s2', s2e - s2)

    s3 = time.time()
    vector1 = [float(counter1_c[k]) for k in all_items] #construit les deux vecteurs pour les ids de tous les keywords des dux séries
    vector2 = [float(counter2_c[k]) for k in all_items]

    s3e = time.time()
    print('s3', s3e - s3)

    return seriename, vector1, vector2

start = time.time()
cur = conn.cursor()
cur.execute(
    "select s.id from recommandation_series s where s.name='Arrow2'")
serie_id = cur.fetchall()[0][0]
#serie_id= Arrow 2 id

cur.execute(
    "select * from mv_{}".format(serie_id))
serie_comparer = cur.fetchall()
#serie_comparer = tous les tf-idfs pour tous les mots clés de arrow2

cur.execute("select s.id from recommandation_series s where s.id <> '{}'".format(serie_id))
others = cur.fetchall()
#others = id de Arrow2

resultat = []
start = time.time()
for other in others:

    cur.execute("select s.name from recommandation_series s where s.id='{}'".format(other[0]))
    seriename = cur.fetchall()[0][0]
    #serieName = nom de Arrow2

    cur.execute("select * from mv_{}".format(other[0]))
    other_words = cur.fetchall()
    #other_words = tous les tfs-idfs et la clé référencant le keyword pour Arrow2

    seriename, v1, v2 = buildVector(seriename, serie_comparer, other_words)

    resultat.append(cosine_distance(seriename, v1, v2))

end = time.time()
print(end-start)
print(sorted(resultat, key=operator.itemgetter(1), reverse=True))
end = time.time()
print('temps total :', end-start)
