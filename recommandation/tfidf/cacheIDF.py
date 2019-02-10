import math
from collections import Counter

from PTUT.settings import DATABASES
import psycopg2
import redis



def lenCollection(cur):
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]


def idf(word, cur):
    cur.execute(
        "SELECT count(s.id) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(
            word))
    documentWithTermCount = cur.fetchall()

    return float(math.log2(lenCollection(cur) / documentWithTermCount[0][0]))


def putIDF_cache():
    r = redis.Redis('localhost')
    conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password=''".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST']))
    cur = conn.cursor()
    cur.execute(
            "SELECT k.key FROM recommandation_keywords as k")
    mots = cur.fetchall()
    for mot in mots:
        r.set(str(mot[0]), str(idf(mot[0], cur)))



putIDF_cache()


