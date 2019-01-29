from django.contrib.auth.models import User
from django.db import models

class Series(models.Model):
    name = models.CharField(max_length=200, unique=True)
    max_keyword_nb = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name



class Rating(models.Model):
    RATE = (
        ('1', '1',),
        ('2', '2',),
        ('3', '3',),
        ('4', '4',),
        ('5', '5',),
    )
    comment = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=1, choices=RATE)
    serie = models.ForeignKey(Series, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)



class KeyWords(models.Model):
    key = models.CharField(max_length=200, unique=True, db_index=True)
    series = models.ManyToManyField(Series, through='Posting')


    def __str__(self):
        return str(self.key) + ' : ' + str(self.series.name)

class Posting(models.Model):
    number = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    keywords = models.ForeignKey(KeyWords, on_delete=models.PROTECT, db_index=True)
    tf = models.DecimalField(max_digits=30, decimal_places=19, null=True)


    def __str__(self):
        return str(self.keywords.key) + ' : ' + str(self.number) + ' : ' + self.series