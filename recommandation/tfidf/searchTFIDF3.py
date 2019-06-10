import operator
import time
from PTUT.settings import DATABASES
import psycopg2
from nltk.stem.snowball import PorterStemmer
import redis

redis_for_similar = redis.Redis(host='localhost', port=6379, db=2)

def calculTf(word, serie_pk):

    cur.execute(
        "SELECT p.tf FROM recommandation_keywords as k, "
        +"recommandation_posting as p, recommandation_series as s "
        +"WHERE s.id = '{0}' AND p.series_id=s.id "
        +"AND p.keywords_id=k.id AND k.key ='{1}'".format(
            serie_pk, word))
    tf = cur.fetchall()
    return tf[0][0]



def idf(word):
    cur.execute(
        "SELECT idf FROM recommandation_keywords as k WHERE k.key = '{}'".format(word))
    resultat = cur.fetchall()

    return resultat[0][0]

def tfIdf(word, liste_series):
    res = dict()
    idf_du_mot = idf(word)

    for serie in liste_series:
        tf = calculTf(word, serie[0])
        cur.execute("SELECT s.name FROM recommandation_series as s WHERE s.id ='{}'".format(serie[0]))
        serie_name = cur.fetchall()


        res[serie_name[0][0]] = tf * idf_du_mot
    return res


conn = psycopg2.connect(
    "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DATABASES['default']['NAME'],
                                                               DATABASES['default']['USER'],
                                                               DATABASES['default']['HOST'],
                                                               DATABASES['default']['PASSWORD']))
cur = conn.cursor()

def search(keywords):
    stemmer = PorterStemmer()
    
    #on sépare la chaine recherchée par mots
    liste_mots = keywords.split(' ')   

    start = time.time()
    dict_res = dict()
    
    #pour chacun de ces mots
    for mot in liste_mots:
        
        #on le stemme pour être cohérent avec ce qui est en base
        mot = stemmer.stem(mot)
        
        #on cherche les ids des séries contenant ce mot
        cur.execute(
            "SELECT s.id FROM recommandation_keywords as k, recommandation_posting as p, "
            +"recommandation_series as s WHERE  p.series_id=s.id "
            +"AND p.keywords_id=k.id AND k.key = '{}'".format(mot))
        liste_series = cur.fetchall()
        
        
        try:
            #res tampon contient un dictionnaire associant le nom 
            #d'une série parmi liste_serie et le tf 
            #du mot actuellement parcouru
            res_tampon = tfIdf(mot, liste_series)
            #key=nom d'une série
            #value=tf-idf
            #pour chacune de ces valeurs
            for key, value in res_tampon.items():
                #On regarde dans dict res si une série du même nom existe déjà
                #si oui
                if dict_res.get(key):
                    #On ajoute dans dict_t res à l'emplacement existant d'une série 
                    #la valeur du tf-idf du mot actuellement parcouru a la somme des tf-idfs 
                    #deja insérés au dictionnaire
                    dict_res[key] = dict_res[key] + value
                #sinon
                else:
                    #on crée une nouvelle entrée dans le dictionnaire clé =nom d'une série, 
                    #valeur = tf-idf
                    dict_res[key] = value
        except:
            pass
    end = time.time()
    print('temps', end - start)
    #on retourne le nom des séries dont la somme des tf-idfs pour les mots recherchés est la plus élevée
    return sorted(dict_res.items(), key=operator.itemgetter(1), reverse=True)




#print(search('medecin chirurgie gallagher'))
