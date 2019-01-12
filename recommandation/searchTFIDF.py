import psycopg2
from sklearn.feature_extraction.text import CountVectorizer

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")



cur = conn.cursor()

cur.execute("SELECT k.key, p.number FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE s.name = 'futurama' AND p.series_id=s.id AND p.keywords_id=k.id")
corpus = cur.fetchall()
D = dict(corpus)
print(len(D))

def calculTf(corpus):
    tfDict = dict()
    lenght = 0
    for key, value in D.items():
        lenght = lenght + value
    for key, value in D.items():
        tfDict[key] = value / lenght
    print(len(tfDict))


#calculTf(D)

def lenCollection():
    cur.execute(
        "SELECT count(*) FROM recommandation_series as s")
    lenCollection = cur.fetchall()
    return lenCollection[0][0]

def idf(word):
    cur.execute(
        "SELECT * FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = 'guerre' AND p.series_id=s.id AND p.keywords_id=k.id")
    corpus = cur.fetchall()
    print(corpus)

idf('toto')



