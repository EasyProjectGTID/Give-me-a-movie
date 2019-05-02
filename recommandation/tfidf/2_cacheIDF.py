import math
from PTUT.settings import DATABASES
import psycopg2

conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password=''".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST']))
cur = conn.cursor()

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
    #print('len de la collection', lenCol)
    #print('document with term', documentWithTermCount)
    #result = float(math.log2(lenCol / documentWithTermCount[0][0]))
    result = float(math.log2(lenCol / 5))

    return round(result,6)


def putIDF_cache():
    cur.execute(
        "SELECT count(k.id) FROM recommandation_keywords as k")
    taille = cur.fetchall()

    cur.execute(
            "SELECT k.id, k.key FROM recommandation_keywords as k")
    mots = cur.fetchall()
    i = 0
    for mot in mots:
        i += 1

        cur.execute("UPDATE recommandation_keywords set idf = '{}' where recommandation_keywords.id = '{}'".format(idf(mot[1]), mot[0]))
        if i % 100 == 0:
            print('{} / {}'.format(i, taille[0][0]))
        #r.set(str(mot[0]), str(idf(mot[0], cur)))

    conn.commit()

lenCol = lenCollection()
putIDF_cache()
# print(idf('survive'))
# print(idf('people'))


