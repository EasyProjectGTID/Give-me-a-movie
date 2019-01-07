import time
import os
from multiprocessing import pool, Process, Manager
from multiprocessing.pool import Pool
import asyncio
import psycopg2
import pysrt
import re

from nltk import PorterStemmer
from nltk.corpus import stopwords
import operator
from collections import Counter

cachedStopWords = stopwords.words("french") + stopwords.words("english")
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password='1777888'")
def getWords(text):
    return re.compile('\w+').findall(text)

def getKey(item):
    return item[1]

def analyseFile(filename, serie):

    subs = pysrt.open(filename, encoding='iso-8859-1')
    list = []
    string = ''
    for i in range(len(subs)):
        for j in getWords(subs[i].text):
            list.append(j.lower())
            string = string + ' ' + j


    # nltk.download('stopwords')
    filtered_words = [word for word in list if word not in cachedStopWords]
    d = Counter(' '.join(filtered_words).split())

    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    cur = conn.cursor()

    list = set()
    for x in sorted_d:
        list.add(x)
    list_sorted = sorted(list, key=getKey)

    for word in list_sorted[-100:]:
        cur.execute(
            "INSERT INTO recommandation_keywords (key) VALUES ('{}') returning id".format(word[0]))
        key_id = cur.fetchone()[0]
        cur.execute("INSERT INTO recommandation_posting (number, keywords_id, series_id) VALUES ('{0}','{1}','{2}')".format(word[1], key_id, serie))
    conn.commit()

def walk_sub():
    conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost'")
    for root in os.scandir("G:\Desktop\sous-titres"):

        cur = conn.cursor()
        cur.execute("INSERT INTO recommandation_series (name) VALUES ('{}') returning id".format(root.name))

        serie_id = cur.fetchone()[0]
        for files in os.scandir(root):
            if str(files.name)[-4:] == '.zip':
                pass
            else:

                analyseFile("G:\Desktop\sous-titres\\" + root.name + '/' + files.name, serie=serie_id)
    conn.close()
import time

start = time.time()
walk_sub()

end = time.time()
print(end - start)




