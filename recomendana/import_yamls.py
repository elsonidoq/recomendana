import os
import re
import yaml
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from recomendana_prof import models


def main():
    if len(sys.argv) < 2: 
        print "usage: python import_yamls.py <yamls_dir>"
        return

    yamls_dir= sys.argv[1]

    with_error= []
    for fname in os.listdir(yamls_dir):
        if not fname.endswith('.yaml'): continue
        fname= os.path.join(yamls_dir, fname)
        print "processing %s" % fname
        process_fname(fname)


def decode_if_not_none(e):
    if e is not None: 
        e= re.sub('\xc2.', '', e)
        # si no, hay un par que no los puede insertar en la db
        return e.decode('ascii', 'ignore')

def process_fname(fname):
    with open(fname) as f:
        data= yaml.load(f)
    
    for i, d in enumerate(data):
        # ignoro los que tienen solo 'id' y 'url'
        if len(d) == 2: continue
        if i % 500 == 0: print '\t',i,'of',len(data)
        m= models.Movie()
        try:
            m.description= decode_if_not_none(d.get('descripcion'))
            m.cast= decode_if_not_none(d.get('reparto'))
            m.genero= decode_if_not_none(d.get('genre'))
            m.subtitles= decode_if_not_none(d.get("subtitulos"))
            m.image= decode_if_not_none(d.get("imagen"))
            m.cuevana_id= int(d.get("id"))
            m.director= decode_if_not_none(d.get("director"))
            m.url= decode_if_not_none(d.get("url"))
            m.title= decode_if_not_none(d.get("titulo"))
            m.language= decode_if_not_none(d.get("idioma"))
            m.producer= decode_if_not_none(d.get("productora"))
            m.popularity= d.get("popularity", -1)
            m.save()
        except Exception, e:
            print "ERROR with id=%s" % d['id']
    


if __name__ == '__main__':
    main()
