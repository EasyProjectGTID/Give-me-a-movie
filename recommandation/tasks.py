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
	subs = walk_sub(MEDIA_ROOT[0])

	serie_id = None
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


def getWords(text):
	return re.findall('\w+', text)


def getKey(item):
	return item[1]


def calculTf(corpus, maxi):
	resultat = dict()
	for word, number in corpus.items():
		resultat[word] = (number, round(number / maxi, 4))
	# print(sorted(resultat.items(), key=operator.itemgetter(1), reverse=True))
	return resultat


def maxNB(corpus):
	return corpus[max(corpus, key=corpus.get)]


def read_srt_files(listSrt):
	corpus = collections.Counter()
	for episode in listSrt:
		subs = pysrt.open(episode, encoding='iso-8859-1')

		stemmer = PorterStemmer()

		tokens = nltk.word_tokenize(subs.text)

		words = [stemmer.stem(unidecode.unidecode(w.lower())) for w in tokens if
				 w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]
		# words = [w.lower() for w in tokens if w.lower() not in cachedStopWords and len(w) > 2 and w.lower().isalpha()]

		corpus.update(words)

	maxi = maxNB(corpus)
	corpusWithTf = calculTf(corpus, maxi)

	return {'corpus': corpusWithTf, 'lenCorpus': maxi}


def insertInDatabase(serieName, corpus, lenCorpus):
	cur = conn.cursor()
	cur.execute("UPDATE recommandation_series  SET max_keyword_nb='{}' WHERE name ='{}'".format(lenCorpus, serieName))
	conn.commit()
	cur.execute("SELECT * from recommandation_series where name = '{}'".format(serieName))
	serie_id = cur.fetchone()[0]

	for word, value in corpus.items():
		# try:
		key_id = cur.execute(
			"INSERT INTO recommandation_keywords (key) VALUES ('{0}') ON CONFLICT (key) DO UPDATE set key='{0}' returning id".format(word))

		key_id = cur.fetchone()[0]

		cur.execute(
			"INSERT INTO recommandation_posting (number, keywords_id, series_id, tf) VALUES ('{0}','{1}','{2}', '{3}')".format(
				value[0], key_id, serie_id, value[1]))
	conn.commit()

	return serie_id


def walk_sub(directory):
	""" Parcours du dossier de sous titres retourne un dictionnaire"""
	seriesPath = dict()
	for root in os.scandir(directory):

		listPath = []
		for racine, dir, files in os.walk(directory + root.name):

			for basename in files:
				if fnmatch.fnmatch(basename, '*.srt'):
					filename = os.path.join(racine, basename)
					listPath.append(filename)

			seriesPath[root.name] = listPath
	return seriesPath


def lenCollection():
	cur = conn.cursor()
	cur.execute(
		"SELECT count(*) FROM recommandation_series as s")
	lenCollection = cur.fetchall()
	return lenCollection[0][0]


def idf(word):
	cur = conn.cursor()
	cur.execute(
		"SELECT count(s.id) FROM recommandation_keywords as k, recommandation_posting as p, recommandation_series as s WHERE k.key = '{}' AND p.series_id=s.id AND p.keywords_id=k.id".format(
			word))
	documentWithTermCount = cur.fetchall()
	# print('len de la collection', lenCol)

	result = math.log2(lenCollection() / documentWithTermCount[0][0])
	return result


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




