import time

from tkiteasy import *
import numpy as np
import pandas as pd
import random
from math import *
from collections import Counter


#on crée le dataframe
pokemon_df = pd.read_csv("pokemon2.csv")
pokemon_df['Level'] = 1
#Dictionnaire qui permet de vérfier si un morpion est gagné:
verification={0:0,1:1,2:2,3:1,4:2}

#Dictionnaire qui associe le nom du pokemon à son numéro

pokeindex={pokemon_df.iloc[i , 1]:pokemon_df.iloc[i , 0] for i in range (pokemon_df.shape[0])}


GX,GY=1400,800
#coord du morpion
X,Y=600,600
#Deuxième écran
sx=GX-X

g=ouvrirFenetre(GX,GY)

#Dictionnaire qui renvoie la coordonnée de la grille
dic={0:(0,0),1:(0,1),2:(0,2),3:(1,0),4:(1,1),5:(1,2),6:(2,0),7:(2,1),8:(2,2)}
#Dictionnaire qui renvoie le numéro de la grille
dicrec={(0,0):0,(0,1):1,(0,2):2,(1,0):3,(1,1):4,(1,2):5,(2,0):6,(2,1):7,(2,2):8}
#Dictionnaire qui renvoie si c'est x ou o ou une case vide
ref={0:"",1:"x",2:"o"}

nombre = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', "ampersand": "1",
          "eacute": "2", "quotedbl": "3", 'apostrophe': "4", 'parenleft': "5", 'section': "6", 'egrave': '7',
          'exclam': '8', 'ccedilla': '9', 'agrave': '0'}

def combat(pokemon1, pokemon2):  # 1v1 entre les Pokémon
    while pokemon1.hp > 0 and pokemon2.hp > 0:
        round_combat(pokemon1, pokemon2)
        #on limite les HP à un minimum de 0
        pokemon1.hp = max(0, pokemon1.hp)
        pokemon2.hp = max(0, pokemon2.hp)

    if pokemon1.hp <= 0 and pokemon2.hp <= 0:
        print("Égalité")
        return None
    elif pokemon1.hp <= 0:
        print(f"{pokemon2.name} a gagné")
        pokemon2.level += 1
        return pokemon2,pokemon1
    else:
        print(f"{pokemon1.name} a gagné")
        pokemon1.level += 1
        return pokemon1,pokemon2


#pokemon 1 attaque le pokemon 2, cette fct calcul les pv perdu par pokemon 2
def attack(pokemon1, pokemon2):
    capa_attak = (((pokemon1.level * 0.4)+2) * pokemon1.attack * pokemon1.sp_atk)
    capa_def = pokemon2.defense
    pv_perdu = np.floor(np.floor(np.floor(capa_attak/capa_def)/50)+2)

    return pv_perdu

def round_combat(pokemon1, pokemon2):
    if pokemon1.dodge() == 'dodge':
        print(f"{pokemon1.name} a esquivé l'attaque, il lui reste {pokemon1.hp} pv")
    else:
        pokemon1.hp -= attack(pokemon2, pokemon1)
        print(f"{pokemon1.name} a pris {attack(pokemon2,pokemon1)} degats, il lui reste {pokemon1.hp} pv")

    if pokemon2.dodge() =='dodge':
        print(f"{pokemon2.name} a esquivé l'attaque, il lui reste {pokemon2.hp} pv")
    else:
        pokemon2.hp -= attack(pokemon1, pokemon2)
        print(f"{pokemon2.name} a pris {attack(pokemon1,pokemon2)} degats, il lui reste {pokemon2.hp} pv")


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
        real_speed = log(self.speed) * (5 / 6)  # on met la speed entre 1,34 et 4,33 grace a la formule
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


class Morpion() :
    def __init__(self,k):
        self.valeur=0
        self.game=True
        self.numero=k
        self.actif=0


    def ajoutcase(self,coord):# coord est la coordonnée du petit morpion dans la grande grille

        self.casier=[]

        # On rajoute les 9 cases du morpion
        for i in range(3):
            ligne = []
            for j in range(3):
                x=coord[0]*3+i
                y=coord[1]*3+j
                a=Case(coord,(i,j),poke.tabgraph[x][y])

                ligne.append(a)
                poke.relation[poke.tabgraph[x][y]]=(coord,(i,j))
                if j==2:

                    self.casier.append(ligne)


    def maj(self):
        for ligne in self.casier:
            for case in ligne :

                if case.valeur==3 or case.valeur==1:
                    g.changerCouleur(case.objet,"olivedrab")
                elif case.valeur==4 or case.valeur==2:
                    g.changerCouleur(case.objet,"peru")


class Case():
    def __init__(self,coord,tu,objet):# coord: coordonné dans la grande grille, tu: coordonnée dans la petite grille
        self.indice=(coord,tu)
        self.valeur=0
        self.objet=objet
        self.pokemon=0
        self.pokecoord=(0,0)

class jeu():
    def __init__(self):
        self.grille=[]
        for i in range (10):
            self.grille.append(Morpion(i))
        self.relation={}
        self.case_plus_jouable=[]
        self.verif=True
        self.num_pokemon=60
        self.case_occupe=[]
        self.poke_on_morpion={}

    # fonction pour équilibrer le nb de pokemons de même type dans les équipes
    def equilibrer_types(self, roster1, roster2):
        print("\nEquilibrage selon les types :\n")
        #on récupère tous les types des Pokémon dans les deux équipes
        types_roster1 = []
        for pokemon in roster1.pokemon_list:
            types_roster1.extend([pokemon.type1, pokemon.type2] if pokemon.type2 else [pokemon.type1])

        types_roster2 = []
        for pokemon in roster2.pokemon_list:
            types_roster2.extend([pokemon.type1, pokemon.type2] if pokemon.type2 else [pokemon.type1])

        # Compter les occurrences des types dans chaque équipe
        count_types_roster1 = Counter(types_roster1)
        count_types_roster2 = Counter(types_roster2)

        # Affichage des comptes de types
        print("Types dans l'équipe 1:", count_types_roster1)
        print("Types dans l'équipe 2:", count_types_roster2)

        # Identifier les types qui sont trop présents
        for type in set(types_roster1 + types_roster2):#on obtient tous les types présents en enlevant les doublons
            difference = count_types_roster1[type] - count_types_roster2[type] #on cherche le nb d occurence dans les dico Counter

            if difference > 1:
                print(f"Le type {type} est trop présent dans le roster 1")
                pokemons_a_deplacer = [pokemon for pokemon in roster1.pokemon_list if
                                       type in [pokemon.type1, pokemon.type2]] #liste de tous les pokemon du type sur représenté
                for pokemon in pokemons_a_deplacer[:difference // 2]: #on prend les diff // 2 premiers pokemons de ceux a deplacer
                    roster1.pokemon_list.remove(pokemon)
                    roster2.pokemon_list.append(pokemon)

            elif difference < -1: # pareil si un type est sur représenté dans le roster2
                print(f"Le type {type} est trop présent dans le roster 2")
                pokemons_a_deplacer = [pokemon for pokemon in roster2.pokemon_list if
                                       type in [pokemon.type1, pokemon.type2]]
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

    # Fonction pour équilibrer les rosters
    # diff = différence maximale de puissance en pourcentage entre les 2 rosters qu'on cherche à avoir
    def balance_rosters(self,roster1, roster2, diff=2):
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
                pokemon_faible = min(roster2.pokemon_list,
                                     key=lambda p: p.total)  # Pokémon le plus faible du roster 2

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

    def delete(self, list):                 #Cette fonction reçoit une liste d'objet graphique et les supprime tous
        for obj in list:
            g.supprimer(obj)

    def Menu(self):                     #Cette fontion est la première qui est appelés quand on lance le jeu après l'ouverture de la fenêtre,
                                        #Elle permet au joueur d'entrer dans le jeu
        self.fond=g.afficherImage(0, 0, "fond.jpg", GX, GY)
        text = [g.afficherImage(0.20*GX,0.35*GY,"T1.png"),
                g.afficherImage(0.15*GX,0.55*GY,"T2.png"),
                g.afficherImage(0.3*GX, 0.7*GY, "Titre.png")]


        a = True
        while a:
            clic = g.attendreClic()
            o = g.recupererObjet(clic.x, clic.y)
            if o == text[2]:                        #Si on clique sur l'image, on rentre dans le jeu, sinon rien ne se passe
                self.delete(text)
                a = False
                self.choices()

    def choices(self):              #Cette fonction permet au joueur de sélectionner le mode de jeu, d'affciher les règles du jeu ou bien d'aller dans les paramètres afin de modifier les paramètres de jeu
        a = True
        graph = [g.afficherImage(GX/6,0.5*GY,"1 vs 1.png"),g.afficherImage(0.6*GX,0.5*GY-20,"Mode IA.png"),g.afficherImage(0.35*GX,0.7*GY,"reg.png"),g.afficherImage(0.3*GX,0.1*GY,"Titre.png")]


        while a:
            o=1
            clic = g.attendreClic()
            try:
                o = g.recupererObjet(clic.x, clic.y)
            except:
                None
            if o!=1:
                if o in graph and o !=graph[3]:
                    self.delete(graph)
                    a = False
                if o == graph[0]:
                    self.jeu_en_duo()
                if o == graph[1]:
                    self.jeu_vs_ia()
                if o==graph[2]:
                    self.settings()
    def settings(self):
        a=True

        text2 = g.afficherTexte(f"{self.num_pokemon}", 0.5 * GX, 0.80 * GY, "Orange", int(GX / 8))
        graph=[g.afficherImage(0.2*GX,GY/2,"nb pok.png"),g.afficherImage(0.02*GX,0.05*GY,'Retour.png'),text2,g.afficherImage(0.7*GX,0.85*GY,"max.png"),g.afficherImage(0.7*GX,0.75*GY,'min.png')]

        while a:
            o=1
            clic = g.recupererClic()
            if clic!=None:
                try:
                    o = g.recupererObjet(clic.x, clic.y)
                except:
                    None

                if o!=1:

                    if o ==graph[0]:
                        ligne=g.dessinerLigne(0.4 * GX, 0.9 * GY,0.6*GX,0.9*GY, "black",10)
                        val = self.changetxt(text2,self.num_pokemon)
                        g.supprimer(ligne)
                        self.num_pokemon=val
                    if o == graph[1]:
                        a=False
                        self.delete(graph)
                        self.choices()

    def changetxt(self, text,val):  # Cette fonction permet de changer le texte en direct sur l'écran, elle renvoie la valeur à la fin de la modification ou
        # la valeur d'avant la modification si la valeur est vide après modification
        ancien = val
        val = str(val)
        tabval = []
        for i in range(len(val)):
            tabval.append(val[i])
        init = tabval

        choix = True
        while choix:
            touche = g.attendreTouche()

            if touche == 'Return':
                choix = False
                if tabval == []:
                    tabval = init

            if touche == "BackSpace":
                if tabval != []:
                    tabval.pop(-1)

            if touche in nombre.keys():
                tabval.append(nombre[touche])

            val = ""

            for i in tabval:
                val += i

            g.changerTexte(text, f"{val}")

        if val == "" or int(val)>80 or int(val)<25:
            g.changerTexte(text, f"{ancien}")
            return ancien
        else:
            return int(val)

    def initgraph(self):
        self.tabgraph=[]
        #Création des cases en graphique
        for i in range (9):
            tab=[]
            for j in range (9):
                rect=g.dessinerRectangle(j*X/9,i*Y/9,X/9,(Y/9)-1,'plum')

                tab.append(rect)
                if j ==8:

                    self.tabgraph.append(tab)

        #Affichage des lignes
        for i in range (1,10):
            couleur = 'white'
            ep=1
            if i%3==0:
                couleur="red"
                ep=4

            g.dessinerLigne(i*X/9,0,i*X/9,Y,couleur,ep=ep)
            g.dessinerLigne(0,i*Y/9,X,i*Y/9,couleur,ep=ep)

        #Mise des images des joeurs:
        g.dessinerLigne(X,GY/2,GX,GY/2,"white",2)

        g.afficherImage(X+sx/2.5,GY/30,"J1.png",200,50)
        g.afficherImage(X+sx/2.5,GY/1.9,"J2.png",200,50)
        g.afficherImage(X+sx/40,0.02*GY,'explique.png')
        j1_col=g.dessinerRectangle(X+0.38*sx,GY/35,0.30*sx,0.1*Y,'olivedrab')
        g.placerAuDessous(j1_col)
        j2_col = g.dessinerRectangle(X + 0.38 * sx, 0.52*GY, 0.30 * sx, 0.1 * Y, 'peru')
        g.placerAuDessous(j2_col)
        try :
            g.placerAuDessous(self.fond)
        except:None

    def calcul_opti(self):#Pour l'affichage des rosters
        if self.num_pokemon % sqrt(self.num_pokemon) == 0:  # Affiche optimal si carré parfait
            self.l = int(sqrt(self.num_pokemon))
        else:  # Sinon
            self.l = int(sqrt(self.num_pokemon) + 1)

        if self.num_pokemon % self.l == 0 and self.num_pokemon % sqrt(self.num_pokemon) != 0:  # Taille des rectangles(coord y)
            self.tercy = 0.75*(GY/2) / (self.l - 1)  # Si Pas besoin d'une ligne pas remplie
        elif self.l ** 2 - self.l > self.num_pokemon:#Pas besoin non plus d'une ligne non remplie
            self.tercy = 0.75 * (GY/2) / (self.l - 1)
        else:
            self.tercy = 0.75 * (GY/2) / (self.l)  # Si besoin d'une ligne non remplie
        self.trecx = 0.85*sx / self.l


    def affichage_des_rosters(self):
        self.calcul_opti()
        # Initialisation des rosters

        self.roster_player1 = Roster(pokemon_df, self.num_pokemon)
        self.roster_player2 = Roster(pokemon_df, self.num_pokemon)
        print(len(self.roster_player1.pokemon_list),'longueur de la liste avant')

        print("\nRoster joueur 1:")
        self.roster_player1.print_roster()
        print("\nRoster joueur 2:")
        self.roster_player2.print_roster()

        # Équilibrage des équipes
        self.balance_rosters(self.roster_player1,self.roster_player2)
        self.equilibrer_types(self.roster_player1,self.roster_player2)
        print(len(self.roster_player1.pokemon_list),'longueur de la liste après')

        self.pokedispo1=[]
        self.pokedispo2=[]
        self.graph1=[]
        self.dicgraph1={}
        a=0
        for y in range(self.l + 1):
            for x in range(self.l):

                if a == self.num_pokemon:  # Si on a atteint le nombre de pokémons, on s'arrête.
                    break

                img=g.afficherImage(x*self.trecx+X+40,y*self.tercy+Y/8+20,f"bw/{pokeindex[self.roster_player1.pokemon_list[a].name]}.png",int(self.trecx),int(self.tercy))
                self.graph1.append(img)
                coordx=x*self.trecx+X+40
                coordy=y*self.tercy+Y/8+20
                self.dicgraph1[img]=(self.roster_player1.pokemon_list[a],coordx,coordy)
                self.pokedispo1.append(self.roster_player1.pokemon_list[a])
                a+=1

        self.graph2=[]
        self.dicgraph2={}
        self.pokedispo2coord={}
        a=0
        for y in range(self.l + 1):
            for x in range(self.l):

                if a == self.num_pokemon:  # Si on a atteint le nombre de pokémons, on s'arrête.
                    break

                img = g.afficherImage(x * self.trecx + X + 40, y * self.tercy + (GY/2)+80,
                                      f"bw/{pokeindex[self.roster_player2.pokemon_list[a].name]}.png", int(self.trecx),
                                      int(self.tercy))
                self.graph2.append(img)
                coordx = x * self.trecx + X + 40
                coordy = y * self.tercy + (GY/2)+80
                self.dicgraph2[img] = (self.roster_player2.pokemon_list[a],coordx,coordy)
                self.pokedispo2.append(self.roster_player2.pokemon_list[a])
                self.pokedispo2coord[self.roster_player2.pokemon_list[a]]=(coordx,coordy)
                a += 1


    def remplissage(self): #Pour chaque petit morpion, on lui rajoute ses cases
        i=0

        for m in self.grille:
            m.ajoutcase(dic[i])
            i+=1
            if i ==9:

                break


    def changement_de_couleur(self,k,couleur):
        for i in range (3):

            for j in range(3):
                g.changerCouleur(self.grille[k].casier[i][j].objet,couleur)

    def verif_morpion(self,morpion):
        en_jeu=True

        #Vérification des lignes
        for ligne in range (3):
            if verification[morpion.casier[ligne][0].valeur] == verification[morpion.casier[ligne][1].valeur] == verification[morpion.casier[ligne][2].valeur] and verification[morpion.casier[ligne][0].valeur] != 0:
                val=verification[morpion.casier[ligne][0].valeur]
                morpion.game=False
                en_jeu = False


        #Vérification des colonnes
        for colonne in range (3):
            if verification[morpion.casier[0][colonne].valeur] == verification[morpion.casier[1][colonne].valeur] == verification[morpion.casier[2][colonne].valeur] and verification[morpion.casier[0][colonne].valeur] != 0:
                val=verification[morpion.casier[0][colonne].valeur]
                morpion.game=False
                en_jeu = False


        #Vérification des diagonales
        if verification[morpion.casier[0][0].valeur]==verification[morpion.casier[1][1].valeur]==verification[morpion.casier[2][2].valeur] and verification[morpion.casier[0][0].valeur]!=0:
            val=verification[morpion.casier[0][0].valeur]
            morpion.game = False
            en_jeu = False


        if verification[morpion.casier[0][2].valeur]==verification[morpion.casier[1][1].valeur]==verification[morpion.casier[2][0].valeur] and verification[morpion.casier[1][1].valeur]!=0:
            val=verification[morpion.casier[0][2].valeur]
            morpion.game = False
            en_jeu = False

        if en_jeu is False:
            morpion.valeur=val

        return en_jeu



    def tour(self,pendule,z=20): #Z est le numéro du morpion où l'on doit jouer
        o=1


        choix=self.choixpokemon(pendule)#(Nom, coordx,coordy)
        while choix is None:
            choix=self.choixpokemon(pendule)
        self.liste=self.affichage_stats(choix[0])


        carre=g.dessinerRectangle(choix[1]+20,choix[2],self.trecx-50,self.tercy,'grey')
        g.placerAuDessous(carre)
        try:g.placerAuDessous(self.fond)
        except:None

        while o ==1:
            clic = g.attendreClic()
            try:
                o = g.recupererObjet(clic.x, clic.y)
            except:
                o=1

        while o in self.dicgraph1 or o in self.dicgraph2:       #Sélection du pokemon
            self.delete(self.liste)
            if pendule % 2 == 0:
                try:
                    if self.dicgraph1[o][0] in self.pokedispo1:
                        choix = self.dicgraph1[o]
                except:None

            else:
                try:
                    if self.dicgraph2[o][0] in self.pokedispo2:
                        choix = self.dicgraph2[o]
                except:None
            self.liste=self.affichage_stats(choix[0])
            g.supprimer(carre)
            carre=g.dessinerRectangle(choix[1]+20,choix[2],self.trecx-50,self.tercy,'grey')
            g.placerAuDessous(carre)
            try:g.placerAuDessous(self.fond)
            except:None
            clic = g.attendreClic()
            try:
                o = g.recupererObjet(clic.x, clic.y)
            except:
                o = 1

        good=True
        while good:
            if o!=1:

                if (o in self.relation.keys() or o in self.poke_on_morpion.values()) and o not in self.case_plus_jouable: #On vérifie que la case est en jeu
                    if o in self.poke_on_morpion.values():
                        o=g.recupererObjetDessous(clic.x,clic.y)

                    a = self.relation[o]
                    if pendule == 0 or self.verif == False:             #Si c'est le premier tour ou cas special, on peut jouer ou on veut
                        self.case_occupe.append(o)
                        case = self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]]

                        good = False
                    else:

                        if self.grille[dicrec[a[0]]].actif == 1:        #On vérifie que la zone à jouer est active
                            self.case_occupe.append(o)
                            case = self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]]

                            good = False
                else:
                    clic = g.attendreClic()
                    try:
                        o = g.recupererObjet(clic.x, clic.y)
                    except:
                        o = 1

            if good is False:#Si la case qu'on joue est jouable, il faut vérifier qu'on affronte une case vide ou adverse mais pas finie
                if pendule%2==0:
                    if case.valeur==3:

                        good=True
                else:
                    if case.valeur==4:

                        good=True

            if good is True:
                clic=g.attendreClic()
                try :
                    o = g.recupererObjet(clic.x, clic.y)
                except:
                    o=1
        #On enlève le pokemon choisi de la liste des pokemons dispo:
        if pendule%2==0:
            self.pokedispo1.remove(choix[0])
        else:
            self.pokedispo2.remove(choix[0])

        #A partir d'ici, on est sur une case jouable donc elle est soit vide,soit déja prise par un pokemon: valeur=3 si joueur 1,4 si joueur 2
        # Coordonée graphique
        x = a[0][0] * X / 3 + a[1][0] * X / 9
        y = a[0][1] * Y / 3 + a[1][1] * Y / 9

        try:
            self.delete(self.liste)
        except:
            None

        if case.valeur==0: #Dans le cas où la case est vide
            # Affichage du pokemon du joueur si le morpion est encore en jeu
            img = g.afficherImage((y + Y / 18) - 36, (x + X / 18) - 40, f"bw/{pokeindex[choix[0].name]}.png",
                                  int((X / 9) * 1.2), int((Y / 9) * 1.2))
            self.poke_on_morpion[a] = img

            case.pokemon = choix[0]
            case.pokecoord = (choix[1], choix[2])
            if pendule%2==0:
                case.valeur = 3
            else:
                case.valeur = 4

        #Deuxième cas, il y a déjà un pokemon sur la case
        else:


            res_fight=combat(case.pokemon,choix[0])#Gagnant en premier, perdant en deuxième
            g.supprimer(self.poke_on_morpion[a])
            del self.poke_on_morpion[a]

            #Le pokemon perdant retourne dans la main, le gagnant disparait
            if res_fight is None:#Match nul, les deux pokemons retournes dans le deck
                tab = [g.recupererObjetDessous2(choix[1]+35, choix[2]+15),g.recupererObjetDessous2(case.pokecoord[0]+35,case.pokecoord[1]+15)]
                self.delete(tab)
                if pendule%2==0:
                    self.pokedispo1.append(choix[0])
                    self.pokedispo2.append(case.pokemon)
                else:
                    self.pokedispo1.append(case.pokemon)
                    self.pokedispo2.append(choix[0])


            elif choix[0]==res_fight[0]:#Le joueur actuel a gagné le combat
                self.graph=self.animation_combat(res_fight[0],res_fight[1])
                objet=g.recupererObjetDessous2(case.pokecoord[0]+35,case.pokecoord[1]+15)
                g.supprimer(objet)
                if pendule%2==0:
                    case.valeur=1
                    self.pokedispo2.append(case.pokemon)
                else:
                    case.valeur=2
                    self.pokedispo1.append(case.pokemon)

            elif choix[0]==res_fight[1]:#Le joeur actuel a perdu le combat
                self.graph=self.animation_combat(res_fight[0],res_fight[1])
                objet = g.recupererObjetDessous2(choix[1]+35, choix[2]+15)
                g.supprimer(objet)

                if pendule%2==0:
                    case.valeur=2
                    self.pokedispo1.append(choix[0])

                else:
                    case.valeur=1
                    self.pokedispo2.append(choix[0])

            if case.valeur==1 or case.valeur==2:
                self.case_plus_jouable.append(case)
                g.afficherTexte(ref[case.valeur], (y + Y / 18), (x + X / 18), "black", 50)



        prochain = dicrec[a[1]]
        if self.grille[prochain].valeur==0: #Si la zone du prochain coup est disponible

            #On remet l'ancienne couleur et on met la nouvelle couleure dans la zone à jouer
            if z!= 20:
                self.changement_de_couleur(dicrec[a[0]],"plum")
            self.changement_de_couleur(dicrec[a[1]],'slateblue')
            self.verif=True

            #On désactive l'ancien morpion et on active le prochain
            self.grille[dicrec[a[0]]].actif = 0
            self.grille[prochain].actif=1

        if self.grille[prochain].valeur!=0:#Si la prochaine zone à jouer n'est pas disponible
            self.changement_de_couleur(dicrec[a[0]], "plum") #Alors on peut jouer n'importe ou sur le jeu
            self.verif=False


        #On vérifie si le petit morpion est terminé
        petitmorpion = self.grille[dicrec[a[0]]]
        if self.verif_morpion(petitmorpion):#pas terminé

            if case.valeur==3:
                g.changerCouleur(case.objet, "olivedrab")
            elif case.valeur==4:
                g.changerCouleur(case.objet, "peru")


        else:#On donne le grand morpion à un joueur

            if petitmorpion.valeur==1:
                couleur="olivedrab"
            else:
                couleur="peru"
            g.dessinerRectangle((a[0][1]*X/3)+2,(a[0][0]*Y/3)+2,(X/3)-4,(Y/3)-4,couleur)
            g.afficherTexte(ref[petitmorpion.valeur],(a[0][1]*Y/3)+Y/6,(a[0][0]*X/3)+X/6,"black",100)
            if self.grille[prochain].valeur!=0:

                self.verif=False

        #On remet de la couleur sur les cases déjà prise
        self.grille[dicrec[a[0]]].maj()
        self.grille[dicrec[a[1]]].maj()


        return prochain

    def returnval(self,i):
        if self.grille[i].valeur == 1:
            val = 1
        else:
            val = 2
        return val
    def verif_fin_jeu(self):
        val=0
        fin=False
        for i in range(0,9,3):#On vérifie les lignes

            if self.grille[i].valeur==self.grille[i+1].valeur==self.grille[i+2].valeur and self.grille[i].valeur!=0:
                fin=True
                val=self.returnval(i)
        for i in range(3):#On vérifie les colonnes
            if self.grille[i].valeur == self.grille[i + 3].valeur == self.grille[i + 6].valeur and self.grille[i].valeur != 0:
                fin=True
                val=self.returnval(i)
        if self.grille[0].valeur==self.grille[4].valeur==self.grille[8].valeur and self.grille[4].valeur!=0:#Première diag
            fin=True
            val=self.returnval(0)
        if self.grille[2].valeur==self.grille[4].valeur==self.grille[6].valeur and self.grille[4].valeur!=0:#Deuxième diag
            fin=True
            val=self.returnval(2)

        return (fin,val)

    def affichage_stats(self,pokemon):
        col="black"
        graph=[g.afficherImage(0.05*X,Y*1.02,"nom.png"),g.afficherImage(X*0.4,Y*1.02,"Type 1.png"),g.afficherImage(X*0.7,Y*1.02,'Type 2.png'),
               g.afficherImage(0.05*X,Y*1.14,"atck.png"),g.afficherImage(X*0.4,Y*1.14,"def.png"),g.afficherImage(X*0.7,Y*1.14,'vitesse.png'),g.afficherImage(0.35*X,Y*1.25,"pv.png")]
        txt=[g.afficherTexte(pokemon.name,0.26*X,Y*1.06,col,sizefont=22),g.afficherTexte(pokemon.type1,X*0.64,Y*1.06,col,sizefont=22),g.afficherTexte(pokemon.type2,X*0.94,Y*1.06,col,sizefont=22),
             g.afficherTexte(pokemon.attack,0.3*X,Y*1.18,col,sizefont=22),g.afficherTexte(pokemon.defense,0.64*X,Y*1.18,col,sizefont=22),g.afficherTexte(pokemon.speed,0.94*X,Y*1.18,col,sizefont=22),
             g.afficherTexte(pokemon.hp,0.49*X,01.28*Y,col,sizefont=22)]
        return graph+txt

    def animation_combat(self,pokemon1,pokemon2):#Le pokemon 1 est le vainqueur du combat
        a = random.randint(0, 1)#Aléatoire pour le placement entre la droite et la gauche
        reverse=False
        if a == 1:
            reverse = True

        if reverse is True:
            poke1=pokemon2
            poke2=pokemon1
        else:
            poke1=pokemon1
            poke2=pokemon2


        graph=[g.afficherImage(0.16*X,1.02*Y,"cl.png"),g.afficherImage(0.45*X,1.15*Y,"vs.png")]
        pokeimg1 = g.afficherImage(0.1 * X, Y * 1.1, f"bw/{pokeindex[poke1.name]}.png")
        pokeimg2 = g.afficherImage(0.7 * X, 1.1 * Y, f"bw/{pokeindex[poke2.name]}.png")
        graph.append(pokeimg1)
        graph.append(pokeimg2)
        g.actualiser()
        g.attendreClic()
        g.supprimer(graph[1])
        graph.remove(graph[1])

        for i in range (25):
            g.actualiser()
            time.sleep(0.01)
            g.deplacer(pokeimg1,8,0)
            g.deplacer(pokeimg2,-8,0)

        g.supprimer(graph[0])
        graph.remove(graph[0])
        gg=g.afficherImage(0.3*X,1.05*Y,"vainqueur.png")
        graph.append(gg)

        if reverse:
            g.supprimer(pokeimg1)
            graph.remove(pokeimg1)
        else:
            g.supprimer(pokeimg2)
            graph.remove(pokeimg2)

        g.actualiser()

        return graph
    def jeu_en_duo(self):
        self.initgraph()
        self.remplissage()
        self.affichage_des_rosters()

        cpt = 0
        a=True
        while a:
            if cpt == 0:
                ancien = self.tour(cpt)
            else:

                ancien = self.tour(cpt, ancien)
            fin_du_jeu=self.verif_fin_jeu()
            if fin_du_jeu[0] is True:
                g.afficherImage(GX / 3, GY / 2, "Merci.png")
                if fin_du_jeu[1]==1:
                    g.afficherImage(0.01 * GX, 0.2 * GY, 'j1win.png')
                else:
                    g.afficherImage(0.01 * GX, 0.2 * GY, 'j2win.png')

                g.afficherImage(GX/2,GY/2,"Merci.png")
                g.actualiser()
                time.sleep(3)
                g.supprimerGFX()
                a=False
                self.Menu()
            cpt += 1

    def jeu_vs_ia(self):
        a=True
        self.initgraph()
        self.remplissage()
        self.affichage_des_rosters()
        first=True
        self.verif=False
        while a:
            if first:
                first=False
                ancien=self.tour_joueur()
            else:
                ancien=self.tour_joueur(ancien)
            try:maj=self.tour_ia(ancien,maj)
            except:maj=self.tour_ia(ancien)#Pour le premier tour
            fin_du_jeu = self.verif_fin_jeu()
            if fin_du_jeu[0] is True:
                g.afficherImage(GX / 3, GY / 2, "Merci.png")
                if fin_du_jeu[1] == 1:
                    g.afficherImage(0.01 * GX, 0.2 * GY, 'j1win.png')
                else:
                    g.afficherImage(0.01 * GX, 0.2 * GY, 'j2win.png')

                g.afficherImage(GX / 2, GY / 2, "Merci.png")
                g.actualiser()
                time.sleep(3)
                g.supprimerGFX()
                a = False
                self.Menu()


    def tour_joueur(self,z=20,pendule=0): #On met pendule a 0 car on joue toujour le joueur 1, jamais le 2
        o = 1

        choix = self.choixpokemon(pendule)  # (Nom, coordx,coordy)
        while choix is None:
            choix = self.choixpokemon(pendule)
        self.liste = self.affichage_stats(choix[0])

        carre = g.dessinerRectangle(choix[1] + 20, choix[2], self.trecx - 50, self.tercy, 'grey')
        g.placerAuDessous(carre)
        try:
            g.placerAuDessous(self.fond)
        except:
            None

        while o == 1:
            clic = g.attendreClic()
            try:
                o = g.recupererObjet(clic.x, clic.y)
            except:
                o = 1
        while o in self.dicgraph1 :       #Sélection du pokemon
            self.delete(self.liste)
            try:
                if self.dicgraph1[o][0] in self.pokedispo1:
                    choix = self.dicgraph1[o]
            except:None

            self.liste=self.affichage_stats(choix[0])
            g.supprimer(carre)
            carre=g.dessinerRectangle(choix[1]+20,choix[2],self.trecx-50,self.tercy,'grey')
            g.placerAuDessous(carre)
            try:g.placerAuDessous(self.fond)
            except:None
            clic = g.attendreClic()
            try:
                o = g.recupererObjet(clic.x, clic.y)
            except:
                o = 1

        good = True
        while good:

            if o != 1:

                if (o in self.relation.keys() or o in self.poke_on_morpion.values()) and o not in self.case_plus_jouable:  # On vérifie que la case est en jeu
                    if o in self.poke_on_morpion.values():
                        o = g.recupererObjetDessous(clic.x, clic.y)

                    a = self.relation[o]
                    if  self.verif == False:  # Si c'est le premier tour ou cas special, on peut jouer ou on veut
                        self.case_occupe.append(o)
                        case = self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]]

                        good = False
                    else:

                        if self.grille[dicrec[a[0]]].actif == 1:  # On vérifie que la zone à jouer est active
                            self.case_occupe.append(o)
                            case = self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]]

                            good = False
                else:
                    clic = g.attendreClic()
                    try:
                        o = g.recupererObjet(clic.x, clic.y)
                    except:
                        o = 1

            if good is False:  # Si la case qu'on joue est jouable, il faut vérifier qu'on affronte une case vide ou adverse mais pas finie
                if case.valeur == 3:
                    good = True

            if good is True:
                clic = g.attendreClic()
                try:
                    o = g.recupererObjet(clic.x, clic.y)
                except:
                    o = 1
        # On enlève le pokemon choisi de la liste des pokemons dispo:

        self.pokedispo1.remove(choix[0])

        # A partir d'ici, on est sur une case jouable donc elle est soit vide,soit déja prise par un pokemon: valeur=3 si joueur 1,4 si joueur 2
        # Coordonée graphique
        x = a[0][0] * X / 3 + a[1][0] * X / 9
        y = a[0][1] * Y / 3 + a[1][1] * Y / 9

        try:
            self.delete(self.liste)
        except:
            None

        if case.valeur == 0:  # Dans le cas où la case est vide
            # Affichage du pokemon du joueur si le morpion est encore en jeu
            img = g.afficherImage((y + Y / 18) - 36, (x + X / 18) - 40,
                                  f"bw/{pokeindex[choix[0].name]}.png",
                                  int((X / 9) * 1.2), int((Y / 9) * 1.2))
            self.poke_on_morpion[a] = img

            case.pokemon = choix[0]
            case.pokecoord = (choix[1], choix[2])
            case.valeur = 3

        # Deuxième cas, il y a déjà un pokemon sur la case
        else:

            self.grille[dicrec[case.indice[0]]].maj()
            res_fight = combat(case.pokemon, choix[0])  # Gagnant en premier, perdant en deuxième
            g.supprimer(self.poke_on_morpion[a])
            del self.poke_on_morpion[a]

            # Le pokemon perdant retourne dans la main, le gagnant disparait
            if res_fight is None:  # Match nul, les deux pokemons retournes dans le deck
                tab = [g.recupererObjetDessous2(choix[1] + 35, choix[2] + 15),
                       g.recupererObjetDessous2(case.pokecoord[0] + 35, case.pokecoord[1] + 15)]
                self.delete(tab)
                self.pokedispo1.append(choix[0])
                self.pokedispo2.append(case.pokemon)



            elif choix[0] == res_fight[0]:  # Le joueur actuel a gagné le combat
                self.graph = self.animation_combat(res_fight[0], res_fight[1])
                objet = g.recupererObjetDessous2(case.pokecoord[0] + 35, case.pokecoord[1] + 15)
                g.supprimer(objet)
                case.valeur = 1
                self.pokedispo2.append(case.pokemon)


            elif choix[0] == res_fight[1]:  # Le joeur actuel a perdu le combat
                self.graph = self.animation_combat(res_fight[0], res_fight[1])
                objet = g.recupererObjetDessous2(choix[1] + 35, choix[2] + 15)
                g.supprimer(objet)
                case.valeur = 2
                self.pokedispo1.append(choix[0])

            if case.valeur == 1 or case.valeur == 2:
                self.case_plus_jouable.append(case)
                g.afficherTexte(ref[case.valeur], (y + Y / 18), (x + X / 18), "black", 50)




        prochain = dicrec[a[1]]
        if self.grille[prochain].valeur == 0:  # Si la zone du prochain coup est disponible

            # On remet l'ancienne couleur et on met la nouvelle couleure dans la zone à jouer
            if z != 20:
                self.changement_de_couleur(dicrec[a[0]], "plum")
            self.changement_de_couleur(dicrec[a[1]], 'slateblue')
            self.verif = True

            # On désactive l'ancien morpion et on active le prochain
            self.grille[dicrec[a[0]]].actif = 0
            self.grille[prochain].actif = 1

        if self.grille[prochain].valeur != 0:  # Si la prochaine zone à jouer n'est pas disponible
            self.changement_de_couleur(dicrec[a[0]], "plum")  # Alors on peut jouer n'importe ou sur le jeu
            self.verif = False

        # On vérifie si le petit morpion est terminé
        petitmorpion = self.grille[dicrec[a[0]]]
        if self.verif_morpion(petitmorpion):  # pas terminé
            if case.valeur == 3:
                g.changerCouleur(case.objet, "olivedrab")

        else:  # On donne le grand morpion à un joueur
            if petitmorpion.valeur == 1:
                couleur = "olivedrab"
            else:
                couleur = "peru"
            g.dessinerRectangle((a[0][1] * X / 3) + 2, (a[0][0] * Y / 3) + 2, (X / 3) - 4, (Y / 3) - 4, couleur)
            g.afficherTexte(ref[petitmorpion.valeur], (a[0][1] * Y / 3) + Y / 6, (a[0][0] * X / 3) + X / 6, "black",
                            100)
            if self.grille[prochain].valeur != 0:
                self.verif = False

        # On remet de la couleur sur les cases déjà prise
        self.grille[dicrec[a[0]]].maj()
        self.grille[dicrec[a[1]]].maj()

        return prochain

    def tour_ia(self,z,misajour=-1):

        try:
            self.grille[misajour].maj()
        except:
            None

        a=len(self.dicgraph2)
        indice=random.randint(0,a)
        pokemon=self.pokedispo2[indice]
        choix=True          #tant qu'on a pas trouvé une case sur laquelle aller, la valeur est True
        while choix is True:
            if self.verif is False:     #On peut aller sur n'importe qu'elle case disponible dans la partie
                gmorp=random.randint(0,8)
                x,y=random.randint(0,2),random.randint(0,2)
                if self.grille[gmorp].casier[x][y].valeur==0 or self.grille[gmorp].casier[x][y].valeur==3:
                    case=self.grille[gmorp].casier[x][y]
                    choix=False
            else:#On peut jouer uniquement dans le petit morpion indiqué par le tour précédent
                x,y=random.randint(0,2),random.randint(0,2)
                if self.grille[z].casier[x][y].valeur==0 or self.grille[z].casier[x][y].valeur==3:
                    case=self.grille[z].casier[x][y]
                    choix=False
        carre=g.dessinerRectangle(self.pokedispo2coord[pokemon][0]+20,self.pokedispo2coord[pokemon][1],self.trecx-50,self.tercy,'grey')
        g.placerAuDessous(carre)
        g.placerAuDessous(self.fond)
        a=case.indice

        x = a[0][0] * X / 3 + a[1][0] * X / 9
        y = a[0][1] * Y / 3 + a[1][1] * Y / 9


        #Maintenant qu'une case à été choisie, soit on pose le pokémon, soit on fait le combat

        if case.valeur == 0:  # Dans le cas où la case est vide
            # Affichage du pokemon du joueur si le morpion est encore en jeu
            img = g.afficherImage((y + Y / 18) - 36, (x + X / 18) - 40,
                                  f"bw/{pokeindex[pokemon.name]}.png",
                                  int((X / 9) * 1.2), int((Y / 9) * 1.2))
            self.poke_on_morpion[a] = img

            case.pokemon = pokemon

            case.pokecoord = (self.pokedispo2coord[pokemon][0],self.pokedispo2coord[pokemon][1])
            case.valeur = 4

        # Deuxième cas, il y a déjà un pokemon sur la case
        else:
            coordx,coordy=self.pokedispo2coord[pokemon][0],self.pokedispo2coord[pokemon][1]

            self.grille[dicrec[case.indice[0]]].maj()
            res_fight = combat(case.pokemon, pokemon)  # Gagnant en premier, perdant en deuxième
            g.supprimer(self.poke_on_morpion[a])
            del self.poke_on_morpion[a]

            # Le pokemon perdant retourne dans la main, le gagnant disparait
            if res_fight is None:  # Match nul, les deux pokemons retournes dans le deck
                tab = [g.recupererObjetDessous2(coordx + 35, coordy + 15),
                       g.recupererObjetDessous2(case.pokecoord[0] + 35, case.pokecoord[1] + 15)]
                self.delete(tab)
                self.pokedispo1.append(pokemon)
                self.pokedispo2.append(case.pokemon)

            elif pokemon == res_fight[0]:  # Le joueur actuel a gagné le combat
                self.graph = self.animation_combat(res_fight[0], res_fight[1])
                objet = g.recupererObjetDessous2(case.pokecoord[0] + 35, case.pokecoord[1] + 15)
                g.supprimer(objet)
                case.valeur = 2
                self.pokedispo1.append(case.pokemon)


            elif pokemon == res_fight[1]:  # Le joeur actuel a perdu le combat
                self.graph = self.animation_combat(res_fight[0], res_fight[1])
                objet = g.recupererObjetDessous2(coordx + 35, coordy + 15)
                g.supprimer(objet)
                case.valeur = 1
                self.pokedispo2.append(pokemon)

            if case.valeur == 1 or case.valeur == 2:
                self.case_plus_jouable.append(case)
                g.afficherTexte(ref[case.valeur], (y + Y / 18), (x + X / 18), "black", 50)

        prochain = dicrec[a[1]]
        if self.grille[prochain].valeur == 0:  # Si la zone du prochain coup est disponible

            # On remet l'ancienne couleur et on met la nouvelle couleure dans la zone à jouer
            if z != 20:
                self.changement_de_couleur(dicrec[a[0]], "plum")
            self.changement_de_couleur(dicrec[a[1]], 'slateblue')
            self.verif = True

            # On désactive l'ancien morpion et on active le prochain
            self.grille[dicrec[a[0]]].actif = 0
            self.grille[prochain].actif = 1

        if self.grille[prochain].valeur != 0:  # Si la prochaine zone à jouer n'est pas disponible
            self.changement_de_couleur(dicrec[a[0]], "plum")  # Alors on peut jouer n'importe ou sur le jeu
            self.verif = False

        # On vérifie si le petit morpion est terminé
        petitmorpion = self.grille[dicrec[a[0]]]
        if self.verif_morpion(petitmorpion):  # pas terminé
            if case.valeur == 4:
                g.changerCouleur(case.objet, "olivedrab")

        else:  # On donne le grand morpion à un joueur
            if petitmorpion.valeur == 1:
                couleur = "olivedrab"
            else:
                couleur = "peru"
            g.dessinerRectangle((a[0][1] * X / 3) + 2, (a[0][0] * Y / 3) + 2, (X / 3) - 4, (Y / 3) - 4, couleur)
            g.afficherTexte(ref[petitmorpion.valeur], (a[0][1] * Y / 3) + Y / 6, (a[0][0] * X / 3) + X / 6, "black",
                            100)
            if self.grille[prochain].valeur != 0:
                self.verif = False

        # On remet de la couleur sur les cases déjà prise
        self.grille[dicrec[a[0]]].maj()
        self.grille[dicrec[a[1]]].maj()

        g.changerCouleur(case.objet,"red")

        return dicrec[case.indice[0]]


    def choixpokemon(self,pendule):
        o=1
        clic=g.attendreClic()
        try:
            o=g.recupererObjet(clic.x,clic.y)
        except:
            None
        if o!=1:

            try:
                self.delete(self.graph)

            except:None
            if o in self.dicgraph1 or o in self.dicgraph2:
                if pendule%2==0:
                    try:
                        if self.dicgraph1[o][0] in self.pokedispo1:
                            choix=self.dicgraph1[o]
                            return choix
                    except:None
                else:
                    try:
                        if self.dicgraph2[o][0] in self.pokedispo2:
                            choix=self.dicgraph2[o]
                            return choix
                    except:None
        self.choixpokemon(pendule)


poke=jeu()

poke.Menu()

g.attendreClic()
g.fermerFenetre()