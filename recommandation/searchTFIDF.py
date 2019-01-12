import math

import psycopg2
from sklearn.feature_extraction.text import CountVectorizer




def calculTf(word, serie_pk):
    tfDict = dict()
    lenght = 0
    cur.execute(
        "SELECT k.key, p.number FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE s.id = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(serie_pk))
    D = dict(cur.fetchall())
    for key, value in D.items():
        lenght = lenght + value
    for key, value in D.items():
        tfDict[key] = value / lenght
    return float(tfDict[word])



def lenCollection():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]

def idf(word):
    cur.execute(
        "SELECT count(*) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(word))
    documentWithTermCount = cur.fetchall()
    return float(math.log10(lenCollection() / documentWithTermCount[0][0]))

def tfIdf(word, liste_series):
    for serie in liste_series:
        tf = calculTf(word, serie[0])
        idff = idf(word)
        cur.execute("SELECT s.name FROM recommandation_series as s WHERE s.id ='{}'".format(serie[0]))
        serie_name = cur.fetchall()
        print(serie_name[0][0], tf * idff)


conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")


cur = conn.cursor()

cur.execute("SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id AND k.key = 'sex'")
liste_series = cur.fetchall()

tfIdf('sex', liste_series)

