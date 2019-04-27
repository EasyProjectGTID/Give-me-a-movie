import operator
import time
from decimal import Decimal

import psycopg2
import numpy
import math
import math
from collections import Counter
from nltk import cluster

def lenCollection():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]

def idf(word):
    cur.execute(
        "SELECT count(s.id) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(word))
    documentWithTermCount = cur.fetchall()
    #print(float(math.log10(lenCollection() / documentWithTermCount[0][0])))
    return 100 * Decimal(math.log2(lenCollection() / documentWithTermCount[0][0]))

def constructIDF(listOfWords):
    newList = []
    for word in listOfWords:

        newList.append((word[0], idf(word[0]) * word[1]))
    return newList

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
def cosine_distance(seriename, u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    return (seriename, Decimal(numpy.dot(u, v)) / Decimal(math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))))


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
    longueur = len(all_items)
    vector1 = [counter1_c[k] for k in all_items]
    vector2 = [counter2_c[k] for k in all_items]

    return seriename, vector1, vector2

start = time.time()
cur = conn.cursor()
cur.execute(
    "select s.id from recommandation_series s where s.name='desperatehousewives'")
serie_id = cur.fetchall()[0][0]

cur.execute(
    "select k.key, p.number from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.id='{}'".format(
        serie_id))
serie_comparer = cur.fetchall()
serie_comparer = constructIDF(serie_comparer)
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
        "select k.key, p.tf from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.id='{}'".format(
            other[0]))
    other_words = cur.fetchall()
    other_words = constructIDF(other_words)
    seriename, v1, v2 = buildVector(seriename, serie_comparer, other_words)

    resultat.append(cosine_distance(seriename, v1, v2))
end = time.time()
print(end-start)
print(sorted(resultat, key=operator.itemgetter(1), reverse=True))
end = time.time()
print('temps total :', end-start)