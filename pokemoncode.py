import pandas as pd
import random
import numpy as np

data=pd.read_csv('pokemon (1).csv')
print(data.head(5))
print(data.columns)

def generateroster(data):
    roster = []
    base = list(range(len(data)))
    for _ in range(60):
        choix = random.choice(base)
        pokemon = data.loc[data.index == choix, 'Name']
        roster.append(pokemon.iloc[0])
        base.remove(choix)

    return roster

def getattributte(pokemon):  #avoir les attributs d'un pokemon dans un dict
    pok = data.loc[data['Name'] == pokemon]
    dict_attribute=pok.iloc[0].to_dict()
    return dict_attribute
def combat(pokemon1,pokemon2):  #1v1 entre les pokemon
    att_pok1=getattributte(pokemon1)
    att_pok2=getattributte(pokemon2)
    round_combat(att_pok1,att_pok2)


#proba que le poke 2 dodge l'attaque du poke 1
def dodge(att_pok1,att_pok2):
    dodge_prob = att_pok2['Sp. Def'] / (att_pok1['Sp. Atk'] +att_pok2['Sp. Def'])
    dodge_coeff=max(0, min(1, dodge_prob))
    random_number = random.randint(1, 100)
    if 0 <= random_number <= np.floor(dodge_prob):
        return 'dodge'
    else:
        return 'get_hit'

#pokemon 1 attaque le pokemon 2, cette fct calcul les pv perdu par pokemon 2
def coup_attak(pokemon1:dict, pokemon2:dict):
    capa_attak=(((pokemon1['Level']*0.4)+2)*pokemon1['Attak']*pokemon1['Sp. Atk'])
    capa_def=pokemon2['Defense']
    pv_perdu=np.floor(np.floor(np.floor(capa_attak/capa_def)/50)+2)

def round_combat(att_pok1,att_pok2):
    if dodge(att_pok1)=='dodge':
        print(f"{att_pok1['Name']} a esquivé l'attaque, il lui reste {att_pok1['HP']} pv")
    else:
        att_pok1['HP']-=coup_attak(att_pok2,att_pok1)
        print(f"{att_pok1['Name']} a pris {coup_attak(att_pok2,att_pok1)} degats, il lui reste {att_pok1['HP']} pv")

    if dodge(att_pok2)=='dodge':
        print(f"{att_pok2['Name']} a esquivé l'attaque, il lui reste {att_pok2['HP']} pv")
    else:
        att_pok2['HP']-=coup_attak(att_pok1,att_pok2)
        print(f"{att_pok2['Name']} a pris {coup_attak(att_pok1,att_pok2)} degats, il lui reste {att_pok2['HP']} pv")


combat('Bulbasaur','Ivysaur')


