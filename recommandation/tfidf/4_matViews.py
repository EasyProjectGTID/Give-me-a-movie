
import psycopg2

from PTUT import DATABASES

conn = psycopg2.connect(
        "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                                DATABASES['default']['USER'],
                                                                DATABASES['default']['HOST'],
                                                                DATABASES['default']['PASSWORD']))
cur = conn.cursor()
#
cur.execute(
    "select s.id, s.name from recommandation_series s")
others = cur.fetchall()
i = 0
for other in others:

    i += 1
    cur.execute(
        "CREATE MATERIALIZED VIEW IF NOT EXISTS  mv_{} "
        "AS select k.key, (p.tf*k.idf) as tfidf from recommandation_keywords k,"
        "recommandation_posting p, recommandation_series s "
        "where k.id = p.keywords_id "
        "AND s.id = p.series_id "
        "AND s.id='{}'".format(str(other[0]),other[0]))
    conn.commit()
    print(i)
#drop
# for i in range(200):
#     print(i)
#     try:
#         cur.execute("DROP MATERIALIZED VIEW mv_{}".format(i))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
