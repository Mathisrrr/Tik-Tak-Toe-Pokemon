#Chaque commentaire sur une ligne seule a pour but d'informer la ligne en dessous
#Chaque commentaire au bout d'une ligne informe sur la ligne elle-même

import pandas as pd
import random

# Charger les données Pokémon
pokemon_df = pd.read_csv("pokemon.csv")

# Classe Pokémon
class Pokemon:
    def __init__(self, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary):
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

    def power_score(self):
        return self.total

    def __str__(self):
        return f"{self.name} ({self.type1}/{self.type2}) - HP: {self.hp}, ATK: {self.attack}, DEF: {self.defense}, SPEED: {self.speed}:"

    # Classe Roster
class Roster:
    def __init__(self, dataframe, num_pokemon):
        self.dataframe = dataframe
        self.num_pokemon = num_pokemon
        self.pokemon_list = self.initialize_roster()

    def initialize_roster(self):
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
                legendary=row['Legendary']
            )
            roster.append(pokemon)
        return roster

    def total_power(self): #Calcule la somme des scores de puissance (self.total) de tous les Pokémon d'un roaster
        return sum(pokemon.total for pokemon in self.pokemon_list)

    def display_roster(self):
        for idx, pokemon in enumerate(self.pokemon_list, start=1):
            print(f"{idx}. {pokemon}")

    # Fonction pour équilibrer les rosters
    # diff = différence maximale de puissance en pourcentage entre les 2 roasters
    def balance_rosters(roster1, roster2, diff=10):

        power1 = roster1.total_power()
        power2 = roster2.total_power()

        while abs(power1 - power2) / max(power1, power2) * 100 > diff :
            # Trouver un Pokémon à échanger
            if power1 > power2:
                # Échanger un Pokémon fort de roster1 avec un faible de roster2
                pokemon_to_give = max(roster1.pokemon_list, key=lambda p: p.power_score())
                pokemon_to_take = min(roster2.pokemon_list, key=lambda p: p.power_score())
            else:
                pokemon_to_give = max(roster2.pokemon_list, key=lambda p: p.power_score())
                pokemon_to_take = min(roster1.pokemon_list, key=lambda p: p.power_score())

            # Échange des Pokémon
            if power1 > power2:
                roster1.pokemon_list.remove(pokemon_to_give)
                roster2.pokemon_list.append(pokemon_to_give)
                roster2.pokemon_list.remove(pokemon_to_take)
                roster1.pokemon_list.append(pokemon_to_take)
            else:
                roster2.pokemon_list.remove(pokemon_to_give)
                roster1.pokemon_list.append(pokemon_to_give)
                roster1.pokemon_list.remove(pokemon_to_take)
                roster2.pokemon_list.append(pokemon_to_take)

            # Recalcul des puissances
            power1 = roster1.total_power()
            power2 = roster2.total_power()

# Initialisation des rosters
num_pokemon = 3  # Modifiable
roster_player1 = Roster(pokemon_df, num_pokemon)
roster_player2 = Roster(pokemon_df, num_pokemon)

# Afficher les puissances initiales
print("Puissance initiale des équipes :")
print(f"Équipe 1 : {roster_player1.total_power()}")
print(f"Équipe 2 : {roster_player2.total_power()}")

# Équilibrage des équipes (Bonus 1/3)
#balance_rosters(roster_player1, roster_player2, threshold=10)
'''
# Afficher les puissances après équilibrage
print("\nPuissance après équilibrage :")
print(f"Équipe 1 : {roster_player1.total_power()}")
print(f"Équipe 2 : {roster_player2.total_power()}")
'''

# Affichage des rosters
print("\nRoster équilibré du joueur 1:")
roster_player1.display_roster()

print("\nRoster équilibré du joueur 2:")
roster_player2.display_roster()