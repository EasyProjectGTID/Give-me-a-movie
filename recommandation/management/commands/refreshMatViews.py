import psycopg2
from django.core.management import BaseCommand

from PTUT import settings

conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(settings.DATABASES['default']['NAME'],
                                                                                settings.DATABASES['default']['USER'],
                                                                                settings.DATABASES['default']['HOST'],
                                                                                settings.DATABASES['default']['PASSWORD']))
class Command(BaseCommand):
	help = 'Refresh des mat views'


	def handle(self, *args, **options):
		cur = conn.cursor()
		#
		cur.execute(
			"select s.id, s.name from recommandation_series s")
		others = cur.fetchall()

		for other in others:
			cur.execute(
				"REFRESH MATERIALIZED VIEW CONCURRENTLY mv_{};".format(str(other[0]), other[0]))
			conn.commit()