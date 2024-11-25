import pandas as pd
import random

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

def dodge(att_pok1):
    proba_dodge=att_pok1['Sp. Def']
    random_number = random.randint(1, 100)
    if 0 <= random_number <= proba_dodge:
        return 'dodge'
    else:
        return 'get_hit'

def round_combat(att_pok1,att_pok2):
    if dodge(att_pok1)=='dodge':
        print(f"{att_pok1['Name']} a esquivé l'attaque, il lui reste {att_pok1['HP']} pv")

    else:
        att_pok1['HP']-=att_pok2['Attack']
        print(f"{att_pok1['Name']} a pris {att_pok2['Attack']} degats, il lui reste {att_pok1['HP']} pv")
    if dodge(att_pok2)=='dodge':
        print(f"{att_pok2['Name']} a esquivé l'attaque, il lui reste {att_pok2['HP']} pv")
    else:
        att_pok2['HP']-=att_pok1['Attack']
        print(f"{att_pok2['Name']} a pris {att_pok1['Attack']} degats, il lui reste {att_pok2['HP']} pv")


combat('Bulbasaur','Ivysaur')


