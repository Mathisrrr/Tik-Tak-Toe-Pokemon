#Chaque commentaire sur une ligne seule a pour but d'informer la ligne en dessous
#Chaque commentaire au bout d'une ligne informe sur la ligne elle-même

import pandas as pd
import random
import numpy as np

#on crée le dataframe
pokemon_df = pd.read_csv("pokemon2.csv")
pokemon_df['Level'] = 1

#class Pokémon
class Pokemon:
    def __init__(self, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary,level):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.generation = generation
        self.legendary = legendary
        self.level = level

    def __str__(self):
        return f"{self.name} ({self.type1}/{self.type2}) - Total: {self.total}, HP: {self.hp}, ATK: {self.attack}, DEF: {self.defense}, SPEED: {self.speed}: LEVEL: {self.level})"

class Roster:
    def __init__(self, dataframe, num_pokemon):
        self.dataframe = dataframe
        self.num_pokemon = num_pokemon
        self.pokemon_list = self.init_roster()

    def init_roster(self): #return une liste d'objects pokemon
        #on choisit num_pokemon lignes du dataframe aléatoirement (.sample)
        sous_dataframe = self.dataframe.sample(self.num_pokemon)
        roster = []
        #iterrows() retourne le tuple (index, ligne(serie en panda)) donc on utilise pas i
        for i, row in sous_dataframe.iterrows(): #on parcours chaque ligne du sous dataframe crée
            pokemon = Pokemon(
                name=row['Name'],
                type1=row['Type 1'],
                type2=row['Type 2'],
                total=row['Total'],
                hp=row['HP'],
                attack=row['Attack'],
                defense=row['Defense'],
                sp_atk=row['Sp. Atk'],
                sp_def=row['Sp. Def'],
                speed=row['Speed'],
                generation=row['Generation'],
                legendary=row['Legendary'],
                level=row['Level']
            )
            roster.append(pokemon)
        return roster

    def total_power(self): #Calcule la somme des scores de puissance (self.total) de tous les Pokémon d'un roaster
        return sum(pokemon.total for pokemon in self.pokemon_list)

    def print_roster(self): #affiche le roster de manière lisible
        print("Puissance Roster",self.total_power())
        for index, pokemon in enumerate(self.pokemon_list, start=1):
            print(f"{index}. {pokemon}")

    # Fonction pour équilibrer les rosters
    # diff = différence maximale de puissance en pourcentage entre les 2 rosters qu'on cherche à avoir
    def balance_rosters(roster1, roster2, diff = 10):
        powerR1 = roster1.total_power()
        powerR2 = roster2.total_power()
        diff_power = round(abs((powerR1 - powerR2) / powerR2) * 100, 2)  # Calcul de la différence de puissance
        print(f"\nPuissances initiales des équipes :\n"
              f"Puissance roster 1: {powerR1}\n"
              f"Puissance roster 2: {powerR2}\n"
              f"Difference de puissance: {diff_power}%\n"
              f"Différence de puissance max: {diff}%")

        max_iterations = 100  # Limite pour éviter une boucle infinie
        cpt = 0  # Compteur
        if diff_power < diff:
            return True

        while diff_power > diff and cpt < max_iterations:
            cpt += 1

            # Identifier les Pokémons à échanger
            if powerR1 > powerR2:  # Roster 1 est plus fort
                pokemon_fort = max(roster1.pokemon_list, key=lambda p: p.total)  # Pokémon le plus fort du roster 1
                pokemon_faible = min(roster2.pokemon_list, key=lambda p: p.total)  # Pokémon le plus faible du roster 2

                # Échange le Pokémon le plus fort de roster 1 contre le Pokémon le plus faible de roster 2
                roster1.pokemon_list.remove(pokemon_fort)
                roster1.pokemon_list.append(pokemon_faible)
                roster2.pokemon_list.append(pokemon_fort)
                roster2.pokemon_list.remove(pokemon_faible)
                print(f"\npokemons echangés:\n{pokemon_faible.name} (roster2 --> roster1) et\n"
                      f"{pokemon_fort.name} (roster1 --> roster2)")


            else:  # Roster 2 est plus fort
                pokemon_fort = max(roster2.pokemon_list, key=lambda p: p.total)
                pokemon_faible = min(roster1.pokemon_list, key=lambda p: p.total)

                # Échange le Pokémon le plus fort de roster 2 contre le Pokémon le plus faible de roster 1
                roster2.pokemon_list.remove(pokemon_fort)
                roster2.pokemon_list.append(pokemon_faible)
                roster1.pokemon_list.append(pokemon_fort)
                roster1.pokemon_list.remove(pokemon_faible)
                print(f"\npokemons echangés:\n{pokemon_faible.name} (roster1 --> roster2) et\n"
                      f"{pokemon_fort.name} (roster2 --> roster1)")

            # Recalcul des puissances
            powerR1 = roster1.total_power()
            powerR2 = roster2.total_power()
            diff_power = round(abs((powerR1 - powerR2) / powerR2) * 100, 2)



        if cpt == max_iterations:
            print("Équilibrage arrêté après avoir atteint la limite d'itérations.")

        print("\nÉquilibrage terminé.")
        print(f"\nPuissances après équilibrage:\n"
              f"Puissance roster 1: {powerR1}\n"
              f"Puissance roster 2: {powerR2}\n"
              f"Difference de puissance: {diff_power}%\n"
              f"Difference de puissance max: {diff}%")

# Initialisation des rosters
num_pokemon = 5 # Modifiable
roster_player1 = Roster(pokemon_df, num_pokemon)
roster_player2 = Roster(pokemon_df, num_pokemon)

# Équilibrage des équipes
Roster.balance_rosters(roster_player1, roster_player2)

# Affichage des rosters
print("\nRoster joueur 1:")
roster_player1.print_roster()
print("\nRoster joueur 2:")
roster_player2.print_roster()

################################
def combat(pokemon1, pokemon2):  # 1v1 entre les Pokémon
    while pokemon1.hp > 0 and pokemon2.hp > 0:
        round_combat(pokemon1, pokemon2)
        #on limite les HP à un minimum de 0
        pokemon1.hp = max(0, pokemon1.hp)
        pokemon2.hp = max(0, pokemon2.hp)

    if pokemon1.hp <= 0 and pokemon2.hp <= 0:
        print("Égalité")
    elif pokemon1.hp <= 0:
        print(f"{pokemon2.name} a gagné")
        pokemon2.level += 1
        return pokemon2
    else:
        print(f"{pokemon1.name} a gagné")
        pokemon1.level += 1
        return pokemon1


#proba que le poke 2 dodge l'attaque du poke 1
def dodge(pokemon1, pokemon2):
    #calcul de la proba de dodge
    dodge_prob = pokemon2.sp_def / (pokemon1.sp_atk + pokemon2.sp_def)
    # Assurer que dodge_prob est entre 0 et 1
    dodge_prob = max(0, min(1, dodge_prob))
    random_nb = random.random() #génère un float entre 0 et 1
    # Déterminer si l'attaque est esquivée ou non
    if random_nb <= dodge_prob:
        return 'dodge'
    else:
        return 'get_hit'

#pokemon 1 attaque le pokemon 2, cette fct calcul les pv perdu par pokemon 2
def attack(pokemon1, pokemon2):
    capa_attak = (((pokemon1.level * 0.4)+2) * pokemon1.attack * pokemon1.sp_atk)
    capa_def = pokemon2.defense
    pv_perdu = np.floor(np.floor(np.floor(capa_attak/capa_def)/50)+2)

    return pv_perdu

def round_combat(pokemon1, pokemon2):
    if dodge(pokemon1) == 'dodge':
        print(f"{pokemon1.name} a esquivé l'attaque, il lui reste {pokemon1.hp} pv")
    else:
        pokemon1.hp -= attack(pokemon2, pokemon1)
        print(f"{pokemon1.name} a pris {attack(pokemon2,pokemon1)} degats, il lui reste {pokemon1.hp} pv")

    if dodge(pokemon2)=='dodge':
        print(f"{pokemon2.name} a esquivé l'attaque, il lui reste {pokemon2.hp} pv")
    else:
        pokemon2.hp -= attack(pokemon1, pokemon2)
        print(f"{pokemon2.name} a pris {attack(pokemon1,pokemon2)} degats, il lui reste {pokemon2.hp} pv")


combat('Bulbasaur','Ivysaur')