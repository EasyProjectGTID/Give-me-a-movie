
import psycopg2

conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
cur = conn.cursor()
#
cur.execute(
    "select s.id, s.name from recommandation_series s")
others = cur.fetchall()
for other in others:


    cur.execute(
        "CREATE MATERIALIZED VIEW IF NOT EXISTS  mv_{} "
        "AS select k.key, (p.tf*k.idf) as tfidf from recommandation_keywords k, recommandation_posting p, recommandation_series s "
        "where k.id = p.keywords_id "
        "AND s.id = p.series_id "
        "AND s.id='{}'".format(str(other[0]),other[0]))
    conn.commit()

#drop
# for i in range(200):
#     print(i)
#     try:
#         cur.execute("DROP MATERIALIZED VIEW mv_{}".format(i))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()