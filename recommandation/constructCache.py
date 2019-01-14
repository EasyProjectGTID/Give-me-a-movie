import math
import operator
import time

import psycopg2

import redis

r = redis.Redis('localhost')
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
cur = conn.cursor()


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


def calcultTfInBDD():
    cur.execute(
        "SELECT p.id, k.key, s.id FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE  p.series_id=s.id AND p.keywords_id=k.id")
    postingALL = cur.fetchall()
    commit = 0
    for post in postingALL:
        tf = calculTf(post[1], post[2])
        cur.execute("UPDATE recommandation_posting p set tf='{}' WHERE p.id='{}'".format(tf, post[0]))
        commit = commit + 1
        if commit % 1000 == 0:
            print(commit)
    conn.commit()

calcultTfInBDD()

