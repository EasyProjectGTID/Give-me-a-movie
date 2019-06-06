import operator
import time
from PTUT.settings import DATABASES
import psycopg2
from nltk.stem.snowball import PorterStemmer
import redis

redis_for_similar = redis.Redis(host='localhost', port=6379, db=2)

def calculTf(word, serie_pk):

    cur.execute(
        "SELECT p.tf FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE s.id = '{0}' AND p.series_id=s.id AND p.keywords_id=k.id AND k.key ='{1}'".format(
            serie_pk, word))
    tf = cur.fetchall()
    return tf[0][0]



def idf(word):
    cur.execute(
        "SELECT idf FROM recommandation_keywords as k WHERE k.key = '{}'".format(word))
    resultat = cur.fetchall()

    return resultat[0][0]

def tfIdf(word, liste_series):
    res = dict()
    idf_du_mot = idf(word)

    for serie in liste_series:
        tf = calculTf(word, serie[0])
        cur.execute("SELECT s.name FROM recommandation_series as s WHERE s.id ='{}'".format(serie[0]))
        serie_name = cur.fetchall()


        res[serie_name[0][0]] = tf * idf_du_mot
    return res


conn = psycopg2.connect(
    "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                               DATABASES['default']['USER'],
                                                               DATABASES['default']['HOST'],
                                                               DATABASES['default']['PASSWORD']))
cur = conn.cursor()

def search(keywords):
    stemmer = PorterStemmer()
    liste_mots = keywords.split(' ')

    start = time.time()
    dict_res = dict()
    for mot in liste_mots:
        #mot = stemmer.stem(mot)
        print(mot)

        cur.execute("SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id AND k.key = '{}'".format(mot))

        liste_series = cur.fetchall()
        print(liste_series)
        try:
            res_tampon = tfIdf(mot, liste_series)

            for key, value in res_tampon.items():
                if dict_res.get(key):
                    dict_res[key] = dict_res[key] + value
                else:
                    dict_res[key] = value
        except:
            pass
    end = time.time()
    print('temps', end - start)
    return sorted(dict_res.items(), key=operator.itemgetter(1), reverse=True)




#print(search('medecin chirurgie gallagher'))
