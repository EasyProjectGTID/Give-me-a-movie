import math
import operator
import time
import psycopg2
from nltk.stem.snowball import FrenchStemmer

from PTUT.settings import DATABASES


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
        tfDict[key] = value / lenght

    return 100 * float(tfDict[word])

def lenCollection():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]

def idf(word):
    cur.execute(
        "SELECT count(s.id) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(word))
    documentWithTermCount = cur.fetchall()
    print(float(math.log10(lenCollection() / documentWithTermCount[0][0])))
    return 100 * float(math.log2(lenCollection() / documentWithTermCount[0][0]))

def tfIdf(word, liste_series):
    res = dict()
    idf_du_mot = idf(word)
    for serie in liste_series:
        tf = calculTf(word, serie[0])
        cur.execute("SELECT s.name FROM recommandation_series as s WHERE s.id ='{}'".format(serie[0]))
        serie_name = cur.fetchall()
        res[serie_name[0][0]] = float(tf * idf_du_mot)
    return res



conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password=''".format(DATABASES['default']['NAME'], DATABASES['default']['USER'], DATABASES['default']['HOST'] ))
cur = conn.cursor()


def search(keywords):

    stemmer = FrenchStemmer()

    liste_mots = keywords.split(' ')
    start = time.time()
    dict_res = dict()
    for mot in liste_mots:
        mot = stemmer.stem(mot)

        cur.execute(
            "SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id AND k.key = '{}'".format(mot))
        liste_series = cur.fetchall()

        res_tampon = tfIdf(mot, liste_series)
        for key, value in res_tampon.items():
            if dict_res.get(key):
                dict_res[key] = dict_res[key] + value
            else:
                dict_res[key] = value


    return sorted(dict_res.items(), key=operator.itemgetter(1), reverse=True)



search('medecin chirurgie gallagher')

