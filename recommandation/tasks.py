import math
import zipfile
import collections
import fnmatch
import os
import nltk
import psycopg2
import pysrt
import re
import requests
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import unidecode
from PTUT.settings import DATABASES, API_KEY, STATIC_URL, STATICFILES_DIRS
from PTUT import HUEY, MEDIA_ROOT
from django.core import management
from recommandation.models import Series
from recommandation.management.commands.loadsubtitles import walk_sub, insertInDatabase, read_srt_files

cachedStopWords = stopwords.words("french") + stopwords.words("english")

conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
																				   DATABASES['default']['USER'],
																				   DATABASES['default']['HOST'],
																				   DATABASES['default']['PASSWORD']))




@HUEY.task()
def file_processing(filename):
	cur = conn.cursor()
	zip_obj = zipfile.ZipFile(MEDIA_ROOT[0] + filename, 'r')
	zip_obj.extractall(MEDIA_ROOT[0])
	zip_obj.close()
	management.call_command('load-subtitles', MEDIA_ROOT[0])

	subs = walk_sub(MEDIA_ROOT[0])  # Ne pas oublier le slash a la fin
	for key, value in subs.items():
		text = read_srt_files(value)
		serie_id = insertInDatabase(key, text['corpus'], text['lenCorpus'])

	print("Téléchargement des infos et des images")
	new_serie = Series.objects.get(id=serie_id)
	URL = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&'
	r = requests.get(URL + 't=' + new_serie.real_name)
	new_serie.name = os.path.splitext(os.path.basename(filename))[0]
	new_serie.infos = r.json()
	new_serie.save()

	response = requests.get(new_serie.infos['Poster'])

	if response.status_code == 200:
		with open(STATICFILES_DIRS[0] + 'posters/' + str(new_serie.name) + '.jpeg', 'wb') as f:
			f.write(response.content)
	new_serie.image_local = STATIC_URL + 'posters/' + str(new_serie.name) + '.jpeg'
	new_serie.save()
	print("Fin Téléchargement des infos et des images")

	management.call_command('cacheIDF')
	print("Creation de la Materialize View")
	cur.execute(
		"CREATE MATERIALIZED VIEW IF NOT EXISTS  mv_{} "
		"AS select k.key, (p.tf*k.idf) as tfidf from recommandation_keywords k, recommandation_posting p, recommandation_series s "
		"where k.id = p.keywords_id "
		"AND s.id = p.series_id "
		"AND s.id='{}'".format(str(serie_id), str(serie_id)))
	conn.commit()
	management.call_command('refreshMatViews')










@HUEY.task()
def getInfos(queryset):
	for serie in queryset:
		URL = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&'
		r = requests.get(URL + 't=' + serie.real_name)
		serie.infos = r.json()
		serie.save()

		try:
			response = requests.get(serie.infos['Poster'])
		except:
			pass

		if response.status_code == 200:
			with open(STATICFILES_DIRS[0] + 'posters/' + str(serie.name) + '.jpeg', 'wb') as f:
				f.write(response.content)
		serie.image_local = STATIC_URL + 'posters/' + str(serie.name) + '.jpeg'
		serie.save()




