os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from random import random
from recomendana_prof import models

def populate():
    tot= models.Movie.objects.count()
    for i, movie in enumerate(models.Movie.objects.all()):
        if i % 100 == 0: print '\t',i,'of',tot
        movie.popularity= 1/random()
        movie.save()

if __name__ == '__main__':
    populate()
