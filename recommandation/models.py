from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import JSONField

class Series(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_keyword_nb = models.IntegerField(blank=True, null=True)
    real_name = models.CharField(max_length=100, blank=True, null=True)
    infos = JSONField(blank=True, null=True)

    def __str__(self):
        if self.real_name:
            return self.real_name
        else:
            return self.name

    class Meta:
        verbose_name_plural = "Series"


class Rating(models.Model):
    RATE = (
        ('1', 'J\'aime'),
        ('0', 'Je n\'aime pas'),

    )
    rating = models.CharField(max_length=1, choices=RATE)
    serie = models.ForeignKey(Series, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)



class KeyWords(models.Model):
    key = models.CharField(max_length=200, unique=True, db_index=True)
    series = models.ManyToManyField(Series, through='Posting')


    def __str__(self):
        return str(self.key)

class Posting(models.Model):
    number = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    keywords = models.ForeignKey(KeyWords, on_delete=models.PROTECT, db_index=True)
    tf = models.DecimalField(max_digits=30, decimal_places=19, null=True)

