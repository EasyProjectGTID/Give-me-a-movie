import psycopg2
from sklearn.feature_extraction.text import CountVectorizer

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")

kw1 = 'sex'
kw2 = 'arme'

cur = conn.cursor()

cur.execute("SELECT k.key, p.number FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE s.name = 'futurama' AND p.series_id=s.id AND p.keywords_id=k.id")
corpus = cur.fetchall()
print(corpus)
from sklearn.feature_extraction.text import CountVectorizer
bag_of_words = CountVectorizer(tokenizer=lambda doc[0]: doc[1], lowercase=False).fit_transform(corpus)
