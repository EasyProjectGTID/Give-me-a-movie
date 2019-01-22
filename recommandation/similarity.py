import psycopg2

import numpy
import math
import math
from collections import Counter
from nltk import cluster
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")

def cosine_distance(u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))



def buildVector():
    cur = conn.cursor()
    cur.execute("select k.key, p.number from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.name='sexandthecity'")
    counter1 = cur.fetchall()

    cur.execute("select k.key, p.number from recommandation_keywords k, recommandation_posting p, recommandation_series s where k.id = p.keywords_id AND s.id = p.series_id AND s.name='weeds'")
    counter2 = cur.fetchall()
    print(counter2)
    # counter1 = dict(counter1)
    # counter2 = dict(counter2)
    # print(counter1)
    # all_items = set(counter1.keys()).union( set(counter2.keys()) )
    #
    # vector1 = [counter1[k] for k in all_items]
    # vector2 = [counter2[k] for k in all_items]
    # return vector1, vector2
    return counter1, counter2
def buildVector1(iterable1, iterable2):
    counter1 = Counter(iterable1)
    counter2= Counter(iterable2)
    print(counter1)
    all_items = set(counter1.keys()).union( set(counter2.keys()) )
    counter1 = dict(counter1)
    vector1 = [counter1[k] for k in all_items]
    print(vector1)
    vector2 = [counter2[k] for k in all_items]
    return vector1, vector2


l1 = "Julie loves me more than Linda loves me coucou coucou".split()
l2 = "Jane likes me more than Julie loves me or".split()

#v1,v2= buildVector1(l1, l2)
print('-----------------')
v1, v2 = buildVector()
#print(cluster.util.cosine_distance(v1,v2))