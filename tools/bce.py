
import requests
import time
from bs4 import BeautifulSoup
import os
import re
import datetime


def parse(value):
    value = value.replace('\t',' ')
    value = value.replace('\n','')
    value = re.sub(' +', ' ', value)
    value = re.compile(r'<[^>]+>').sub('', value)
    return value.lstrip().rstrip()

def get_data_from_bce(nbce):
    nbce = nbce.replace('.','').replace(' ','').replace('-','')
    out = {}
    url = 'https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=%s&actionLu=Recherche&lang=fr' % nbce
    soup = BeautifulSoup(requests.get(url).content, features="html.parser")
    for row in soup.findAll('tr'):
        #print(row)
        cols = row.findAll("td")
        if len(cols) >=2 :
            field = cols[0].text
            value = cols[1].text
            if "Statut" in field:
                out['statut'] = parse(value)
            elif "Situation" in field :
                value = value.split('Depuis')[0]
                out['situation_juridique'] = parse(value)
            elif "Date de début" in field:
                mois = {'janvier':'1', 'février':'2', 'mars':'3', 'avril':'4', 'mai':'5', 'juin':'6', 'juillet':'7', 'aout':'8', 'août':'8', 'septembre':'9', 
                        'octobre':'10', 'novembre':'11', 'décembre':'12', 'decembre':'12'}
                s = parse(value).split(' ')
                date = datetime.date(int(s[2]), int(mois[s[1]]),int(s[0]))
                out['date_debut'] = date
            elif "Dénomination" in field:
                value = value.split('Dén')[0]
                out['denomination'] = parse(value)
            elif "Adresse du siège" in field:
                adr = value.split('<br>')[0].split('\n')
                res = adr[1].split('\xa0')
                out['adresse'] = parse(res[0])
                if len(res) == 2:
                    out['adresse_num'] = parse(res[1])
                res = adr[2].split('\xa0')
                out['adresse_cp'] = parse(res[0])
                if len(res) == 2:
                    out['adresse_ville'] = parse(res[1])
            elif "Forme" in field:
                value = value.split('Depuis')[0]
                out['forme_legale'] = parse(value)
            elif "Gérant" in field or "Administrateur" in field :
                print(parse(field))
                print(parse(value))
            elif "Date de fin de l'année comptable" in field:
                out['date_fin_annee_comptable'] = parse(value)
    #print(out)
    return out