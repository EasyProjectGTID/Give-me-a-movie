from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.safestring import mark_safe


class Series(models.Model):
	name = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name='Nom du dossier')
	max_keyword_nb = models.IntegerField(blank=True, null=True, verbose_name='Max du mot le plus cité')
	real_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nom de la serie')
	infos = JSONField(blank=True, null=True, verbose_name='Informations complémentaires')
	image_local = models.ImageField(null=True, blank=True)

	def __str__(self):
		if self.real_name:
			return self.real_name
		else:
			return self.name

	def image(self):
		return mark_safe('<img src="{}" width="75" />'.format(self.image_local))

	class Meta:
		verbose_name = 'Une serie'
		verbose_name_plural = 'Les series'


class SearchCount(models.Model):
	search_key = models.CharField(max_length=35, null=True, unique=True, verbose_name='Mot de recherche')
	count = models.IntegerField(verbose_name='Nombre de recherche')

	def __str__(self):
		return self.search_key + ' Nombre de recherche : ' + str(self.count)

	class Meta:
		verbose_name = 'Recherche'
		verbose_name_plural = 'Les recherches'


class Rating(models.Model):
	RATE = (
		('1', 'J\'aime'),
		('0', 'Je n\'aime pas'),

	)
	rating = models.CharField(max_length=1, choices=RATE, verbose_name='Notation')
	serie = models.ForeignKey(Series, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Utilisateur')
	date_vote = models.DateTimeField(auto_now=True, verbose_name='Date de vote')

	class Meta:
		unique_together = (("rating", "serie", "user"),)
		verbose_name = 'Le vote'
		verbose_name_plural = 'Les votes'

	def __str__(self):
		return self.user.username + ' a voté ' + self.get_rating_display() + ' ' + self.serie.__str__()


class KeyWords(models.Model):
	key = models.CharField(max_length=200, unique=True, db_index=True, verbose_name='Mot')
	#series = models.ManyToManyField(Series, through='Posting', verbose_name='Serie')
	idf = models.FloatField(null=True, verbose_name='Inverse document Frequency')

	def __str__(self):
		return str(self.key)

	class Meta:
		verbose_name = 'Mot'
		verbose_name_plural = 'Les mots des sous titres'


class Posting(models.Model):
	number = models.IntegerField(verbose_name='Nombre de fois que le mot est cité')
	series = models.ForeignKey(Series, on_delete=models.CASCADE, verbose_name='Serie')
	keywords = models.ForeignKey(KeyWords, on_delete=models.CASCADE, db_index=True, verbose_name='Mot')
	tf = models.FloatField(null=True, verbose_name='Term Frequency')

	class Meta:
		verbose_name = 'Mot cité dans une serie'
		verbose_name_plural = 'Corpus des series'


class Similarity(models.Model):
	serie = models.ForeignKey(Series, null=True, on_delete=models.CASCADE, related_name='serie')
	similar_to = models.ForeignKey(Series, null=True, on_delete=models.CASCADE, related_name='similar_to')
	score = models.FloatField(null=True)

	class Meta:
		verbose_name = 'Similaire'
		verbose_name_plural = 'Similarités'


