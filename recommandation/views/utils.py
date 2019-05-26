from django.db import IntegrityError

from recommandation.models import Rating
from recommandation.models import SearchCount


def afficheVoteFn(user, serie):
	rating = Rating.objects.filter(user=user, serie=serie).exists()
	if rating:
		afficheVote = False
	else:
		afficheVote = True

	return afficheVote

def recherche_history(text):
	text_split = text.split(' ')
	for word in text_split:
		try:
			SearchCount.objects.create(search_key=word, count=1)
		except IntegrityError:
			search_obj = SearchCount.objects.get(search_key=word)
			search_obj.count = search_obj.count + 1
			search_obj.save()


