#Chaque commentaire sur une ligne seule a pour but d'informer la ligne en dessous
#Chaque commentaire au bout d'une ligne informe sur la ligne elle-même

import pandas as pd
import random
import numpy as np
import math
from collections import Counter


#VARIABLES GLOBALES
nb_pokemon = 60

#on crée le dataframe
pokemon_df = pd.read_csv("pokemon2.csv")
pokemon_df['Level'] = 1
pokemon_df['Type 2'] = pokemon_df['Type 2'].fillna("") #on remplace tout les types 2 manquants par le caractère vide


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

    def dodge_chance(self):  # return une chance d'esquive en %
        # speed comprises entre 5 et 180 dans le excel
        real_speed = math.log(self.speed) * (5 / 6)  # on met la speed entre 1,34 et 4,33 grace a la formule
        # formule choisie arbitrairement qui permet d'avoir des taux d'esquives pas trop abusés
        dodge_rate = real_speed * 10  # on obtient un dodge rate de 13,4 à 43,3%
        return dodge_rate

    def dodge(self):  # return True si esquive, False si pas esquive
        dodge = False
        dodge_rate = self.dodge_chance()  # taux d'esquive en pourcentage
        random_nb = random.uniform(0, 100)
        if random_nb <= dodge_rate:  # esquive si le nombre aléatoire est inférieur au taux
            dodge = True
        return dodge

    def type_multiplier(self,attacker_type1, attacker_type2, defender_type1, defender_type2):
        #Tableau des multiplicateurs de degats en fonction des différents types
        coef_type = {
            "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
            "Fire": {"Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Steel": 2.0, "Fire": 0.5, "Water": 0.5, "Rock": 0.5,
                     "Dragon": 0.5},
            "Water": {"Fire": 2.0, "Ground": 2.0, "Rock": 2.0, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
            "Electric": {"Water": 2.0, "Flying": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Dragon": 0.5},
            "Grass": {"Water": 2.0, "Ground": 2.0, "Rock": 2.0, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5,
                      "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
            "Ice": {"Grass": 2.0, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Fire": 0.5, "Water": 0.5, "Ice": 0.5,
                    "Steel": 0.5},
            "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0, "Poison": 0.5,
                         "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5, "Ghost": 0.0},
            "Poison": {"Grass": 2.0, "Fairy": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5,
                       "Steel": 0.0},
            "Ground": {"Fire": 2.0, "Electric": 2.0, "Poison": 2.0, "Rock": 2.0, "Steel": 2.0, "Grass": 0.5, "Bug": 0.5,
                       "Flying": 0.0},
            "Flying": {"Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
            "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Steel": 0.5, "Dark": 0.0},
            "Bug": {"Grass": 2.0, "Psychic": 2.0, "Dark": 2.0, "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5,
                    "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
            "Rock": {"Fire": 2.0, "Ice": 2.0, "Flying": 2.0, "Bug": 2.0, "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
            "Ghost": {"Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Normal": 0.0},
            "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
            "Dark": {"Psychic": 2.0, "Ghost": 2.0, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
            "Steel": {"Ice": 2.0, "Rock": 2.0, "Fairy": 2.0, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
            "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
        }

        #calculer le multiplicateur pour un seul type
        def single_type_multiplier(type_poke_attack, type_poke_defend):
            if type_poke_attack == "" or type_poke_defend == "":  # Si l'un des types est = au caractère vide
                return 1
            return coef_type.get(type_poke_attack).get(type_poke_defend, 1) #on met le 1 pour quand le type d'attaque et de défense n'ont pas de coef multiplicateur particulier

        #multiplicateurs en fonction des 2 types de chaque pokemon (double distributivitée)
        multiplier1 = single_type_multiplier(attacker_type1, defender_type1)
        multiplier2 = single_type_multiplier(attacker_type1, defender_type2)
        multiplier3 = single_type_multiplier(attacker_type2, defender_type1)
        multiplier4 = single_type_multiplier(attacker_type2, defender_type2)

        # Produit des multiplicateurs
        total_multiplier = multiplier1 * multiplier2 * multiplier3 * multiplier4
        return total_multiplier

    def attack_(self, pokemon2):
        #le pokemon (self) attaque le pokemon adverse (pokemon2), cette fct calcul combien de pv le pokemon adverse va perdre
        chance = random.uniform(0.85, 1.15) #la chance peut reduire ou augmenter de 15% maximum les degats infligés
        capa_attak = (((self.level * 1.2) + 2) * self.attack + 0.2 * self.sp_atk) * chance
        capa_def = pokemon2.defense * 0.1
        multiplicateur = self.type_multiplier(self.type1, self.type2, pokemon2.type1, pokemon2.type2)
        degats = (np.floor(np.floor(capa_attak / capa_def) / 2) + 2  ) * multiplicateur

        return degats

class Roster:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.num_pokemon = nb_pokemon
        self.pokemon_list = self.init_roster()

    def init_roster(self): #return une liste d'objects pokemon
        #on choisit {nb_pokemon lignes} du dataframe aléatoirement (.sample)
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

class Jeu:
    def __init__(self):
        self.a = 0

    # Fonction pour équilibrer les rosters
    # diff = différence maximale de puissance en pourcentage entre les 2 rosters qu'on cherche à avoir
    def balance_rosters(self,roster1, roster2, diff=10):
        powerR1 = roster1.total_power()
        powerR2 = roster2.total_power()
        diff_power = round(abs((powerR1 - powerR2) / powerR2) * 100, 2)  # Calcul de la différence de puissance
        print(f"\nPuissances initiales des équipes :\n"
              f"Puissance roster 1: {powerR1}\n"
              f"Puissance roster 2: {powerR2}\n"
              f"Difference de puissance: {diff_power}%\n"
              f"Différence de puissance max: {diff}%")

        max_iterations = 10  # Limite pour éviter une boucle infinie
        cpt = 0  # Compteur
        if diff_power < diff:
            return True

        while diff_power > diff and cpt < max_iterations:
            cpt += 1
            # Identifier les Pokémons à échanger
            if powerR1 > powerR2:  # Roster 1 est plus fort
                pokemon_fort = max(roster1.pokemon_list, key=lambda p: p.total)  # Pokémon le plus fort du roster 1
                pokemon_faible = min(roster2.pokemon_list,
                                     key=lambda p: p.total)  # Pokémon le plus faible du roster 2

                # Échange le Pokémon le plus fort de roster 1 contre le Pokémon le plus faible de roster 2
                roster1.pokemon_list.remove(pokemon_fort)
                roster1.pokemon_list.append(pokemon_faible)
                roster2.pokemon_list.append(pokemon_fort)
                roster2.pokemon_list.remove(pokemon_faible)
                print(f"\npokemons echangés:\n{pokemon_faible.name} (roster2 --> roster1)\n"
                      f"{pokemon_fort.name} (roster1 --> roster2)")

            else:  # Roster 2 est plus fort
                pokemon_fort = max(roster2.pokemon_list, key=lambda p: p.total)
                pokemon_faible = min(roster1.pokemon_list, key=lambda p: p.total)

                # Échange le Pokémon le plus fort de roster 2 contre le Pokémon le plus faible de roster 1
                roster2.pokemon_list.remove(pokemon_fort)
                roster2.pokemon_list.append(pokemon_faible)
                roster1.pokemon_list.append(pokemon_fort)
                roster1.pokemon_list.remove(pokemon_faible)
                print(f"\npokemons echangés:\n{pokemon_faible.name} (roster1 --> roster2)\n"
                      f"{pokemon_fort.name} (roster2 --> roster1)")

            # Recalcul des puissances
            powerR1 = roster1.total_power()
            powerR2 = roster2.total_power()
            diff_power = round(abs((powerR1 - powerR2) / powerR2) * 100, 2)

        if cpt == max_iterations:
            print("\nÉquilibrage arrêté après avoir atteint la limite d'itérations.")

        print("\nÉquilibrage terminé.")
        print(f"\n--- Puissances après équilibrage: ---\n\n"
              f"Puissance roster 1: {powerR1}\n"
              f"Puissance roster 2: {powerR2}\n"
              f"Difference de puissance: {diff_power}%\n"
              f"Difference de puissance max: {diff}%")

    def obtenir_types(self, pokemon):
        return [pokemon.type1, pokemon.type2] if pokemon.type2 else [pokemon.type1]

    #fonction pour équilibrer le nb de pokemons de même type dans les équipes
    def equilibrer_types(self, roster1, roster2):
        print("\nEquilibrage selon les types :\n")
        # Récupérer tous les types des Pokémon dans les deux équipes
        types_roster1 = []
        for pokemon in roster1.pokemon_list:
            types_roster1.extend([pokemon.type1, pokemon.type2] if pokemon.type2 else [pokemon.type1])

        types_roster2 = []
        for pokemon in roster2.pokemon_list:
            types_roster2.extend([pokemon.type1, pokemon.type2] if pokemon.type2 else [pokemon.type1])

        # Compter les occurrences des types dans chaque équipe
        count_types_equipe1 = Counter(types_roster1)
        count_types_equipe2 = Counter(types_roster2)

        # Affichage des comptes de types
        print("Types dans l'équipe 1:", count_types_equipe1)
        print("Types dans l'équipe 2:", count_types_equipe2)

        # Identifier les types qui sont trop présents
        for type_ in set(types_roster1 + types_roster2):
            difference = count_types_equipe1[type_] - count_types_equipe2[type_]

            if difference > 1:
                print(f"Le type {type_} est trop présent dans le roster 1")
                pokemons_a_deplacer = [pokemon for pokemon in roster1.pokemon_list if
                                       type_ in [pokemon.type1, pokemon.type2]]
                for pokemon in pokemons_a_deplacer[:difference // 2]:
                    roster1.pokemon_list.remove(pokemon)
                    roster2.pokemon_list.append(pokemon)

            elif difference < -1:
                print(f"Le type {type_} est trop présent dans le roster 2")
                pokemons_a_deplacer = [pokemon for pokemon in roster2.pokemon_list if
                                       type_ in [pokemon.type1, pokemon.type2]]
                for pokemon in pokemons_a_deplacer[:(-difference) // 2]:
                    roster2.pokemon_list.remove(pokemon)
                    roster1.pokemon_list.append(pokemon)

        # Ajustement des tailles des équipes
        while len(roster1.pokemon_list) > len(roster2.pokemon_list):
            pokemon = random.choice(roster1.pokemon_list)
            roster1.pokemon_list.remove(pokemon)
            roster2.pokemon_list.append(pokemon)

        while len(roster2.pokemon_list) > len(roster1.pokemon_list):
            pokemon = random.choice(roster2.pokemon_list)
            roster2.pokemon_list.remove(pokemon)
            roster1.pokemon_list.append(pokemon)

        print("\nEquilibrage selon les types fini")
        return roster1, roster2

    def round_combat(self,pokemon1, pokemon2):
        if pokemon1.dodge() == True:
            print(f"{pokemon1.name} a esquivé l'attaque, il lui reste {pokemon1.hp} pv")
        else: #attaque du pokemon 2 sur le 1
            degats = pokemon2.attack_(pokemon1)
            pokemon1.hp -= degats
            pokemon1.hp = max(0, pokemon1.hp)
            print(f"{pokemon1.name} a pris {degats} degats, il lui reste {pokemon1.hp} pv")

        if pokemon2.dodge() == True:
            print(f"{pokemon2.name} a esquivé l'attaque, il lui reste {pokemon2.hp} pv")
        else: #attaque du pokemon 1 sur le 2
            degats = pokemon1.attack_(pokemon2)
            pokemon2.hp -= degats
            pokemon2.hp = max(0, pokemon2.hp)
            print(f"{pokemon2.name} a pris {degats} degats, il lui reste {pokemon2.hp} pv")

    def unVSun(self, pokemon1, pokemon2):  # 1v1 entre les Pokémon
        cpt=1
        while pokemon1.hp > 0 and pokemon2.hp > 0:
            print("\nTour ",cpt)
            cpt += 1
            self.round_combat(pokemon1, pokemon2)

        if pokemon1.hp == 0 and pokemon2.hp == 0:
            print("Égalité")
            return True

        elif pokemon1.hp == 0:
            print(f"\n{pokemon2.name} a gagné")
            pokemon1.level += 1
            return pokemon1, pokemon2 #pokemon qui a perdu en premier (donc celui qu'on garde)

        else:
            print(f"{pokemon1.name} a gagné")
            pokemon2.level += 1
            return pokemon2, pokemon1 #pokemon qui a perdu en premier

    def choose_fighter(self):
        a=0
        #recup clic de l'image du pokemon qu'on veut choper (ou le nom)


# Initialisation des rosters
jeu = Jeu()
roster_player1 = Roster(pokemon_df)
roster_player2 = Roster(pokemon_df)
print("\nRoster joueur 1:")
roster_player1.print_roster()

print("\nRoster joueur 2:")
roster_player2.print_roster()

# Équilibrage des équipes
jeu.equilibrer_types(roster_player1, roster_player2)
jeu.balance_rosters(roster_player1, roster_player2)


# Affichage des rosters
print("\nRoster joueur 1:")
roster_player1.print_roster()

print("\nRoster joueur 2:")
roster_player2.print_roster()
a=jeu.unVSun(roster_player1.pokemon_list[0],roster_player2.pokemon_list[0])