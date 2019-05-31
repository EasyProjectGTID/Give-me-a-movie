from PTUT import STATICFILES_DIRS, STATIC_URL
from recommandation.models import Series
import requests

def download():
	series = Series.objects.all()
	for serie in series:

		print(serie.real_name)
		print(serie.infos['Poster'])
		response = requests.get(serie.infos['Poster'])

		if response.status_code == 200:
			with open(STATICFILES_DIRS[0] + 'posters/' + str(serie.name) + '.jpeg', 'wb') as f:
				f.write(response.content)
		serie.image_local = STATIC_URL  + 'posters/' + str(serie.name) + '.jpeg'
		serie.save()
