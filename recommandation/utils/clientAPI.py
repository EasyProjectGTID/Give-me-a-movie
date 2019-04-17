import requests
from PTUT.settings import API_KEY

def getInfos():

        URL = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&'
        r = requests.get(URL + 't=' + 'weeds')
        print(URL + 't=' + 'weeds')
        print(r.json())

getInfos()