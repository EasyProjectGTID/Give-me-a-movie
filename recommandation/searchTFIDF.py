import math
import operator
import time

import psycopg2

import redis

r = redis.Redis('localhost')

REDIS = False


def calculTf(word, serie_pk):
    tfDict = dict()
    lenght = 0
    cur.execute(
        "SELECT k.key, p.number FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE s.id = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(
            serie_pk))
    D = dict(cur.fetchall())

    for key, value in D.items():
        lenght = lenght + value
    for key, value in D.items():
        # tfDict[key] = value / lenght
        tfDict[key] = value / lenght

    return float(tfDict[word])


def lenCollection():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]


def idf(word):
    cur.execute(
        "SELECT count(s.id) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(
            word))
    documentWithTermCount = cur.fetchall()
    if REDIS:
        return float(math.log10(float(r.get("countCollection")) / documentWithTermCount[0][0]))
    else:

        return 100 * float(math.log2(lenCollection() / documentWithTermCount[0][0]))


def tfIdf(word, liste_series):
    res = {}
    for serie in liste_series:
        tf = calculTf(word, serie[0])
        idff = idf(word)

        cur.execute("SELECT s.name FROM recommandation_series as s WHERE s.id ='{}'".format(serie[0]))
        serie_name = cur.fetchall()
        res[serie_name[0][0]] = float(tf * idff)
    #print(sorted(res))
    return res

def cache():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    r.set("countCollection", lenCollection[0][0])


conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
cur = conn.cursor()

# cur.execute(
#     "SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id AND k.key = 'police'")
# liste_series = cur.fetchall()
#
# start = time.time()
# tfIdf('police', liste_series)
# end = time.time()
# print(end - start)


mots = 'police mackey'
liste_mots = mots.split(' ')
print(liste_mots)

dict_res = {}
for mot in liste_mots:
    cur.execute(
        "SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id AND k.key = '{}'".format(mot))
    liste_series = cur.fetchall()
    res_tampon = tfIdf(mot, liste_series)
    for key, value in res_tampon.items():
        if dict_res.get(key):
            dict_res[key] = dict_res[key] + value
        else:
            dict_res[key] = value
print(sorted(dict_res.items(), key=operator.itemgetter(1)))