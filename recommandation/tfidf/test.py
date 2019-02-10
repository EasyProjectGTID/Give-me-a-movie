import psycopg2

from sklearn.feature_extraction.text import TfidfVectorizer

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")

cur = conn.cursor()
cur.execute(
    "select s.id from recommandation_series s where s.name='sexandthecity'")
serie_id = cur.fetchall()[0][0]

cur.execute(
    "select k.key, p.number from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.id='{}'".format(
        serie_id))
serie_comparer = cur.fetchall()

