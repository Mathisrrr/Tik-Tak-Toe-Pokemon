from tkiteasy import *
import numpy as np
import pandas as pd
import random

#on crée le dataframe
pokemon_df = pd.read_csv("pokemon2.csv")
pokemon_df['Level'] = 1

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

                if case.valeur!=0:
                    g.changerCouleur(case.objet,"olivedrab")


class Case():
    def __init__(self,coord,tu,objet):# coord: coordonné dans la grande grille, tu: coordonnée dans la petite grille
        self.indice=(coord,tu)
        self.valeur=0
        self.objet=objet

class jeu():
    def __init__(self):
        self.grille=[]
        for i in range (10):
            self.grille.append(Morpion(i))
        self.relation={}
        self.dejapris=[]
        self.verif=True

    def delete(self, list):                 #Cette fonction reçoit une liste d'objet graphique et les supprime tous
        for obj in list:
            g.supprimer(obj)

    def Menu(self):                     #Cette fontion est la première qui est appelés quand on lance le jeu après l'ouverture de la fenêtre,
                                        #Elle permet au joueur d'entrer dans le jeu
        g.afficherImage(0, 0, "fond.jpg", GX, GY)
        text = [g.afficherTexte("Bienvenue dans le jeu Poké-Tac-Toe", GX / 2, 2 * GY / 5, "Black", int(GX / 22)),
                g.afficherTexte("Cliquez sur l'image pour afficher les modes de jeu", GX / 2, GY / 2, 'Black',
                                     int(GX / 30)),
                g.afficherImage(0.3*GX, 0.6*GY, "Titre.png")]

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
        graph=[g.afficherImage(0.2*GX,GY/2,"nb pok.png"),g.afficherImage(0.02*GX,0.05*GY,'Retour.png')]

        while a:
            o=1
            clic = g.recupererClic()
            if clic!=None:
                try:
                    o = g.recupererObjet(clic.x, clic.y)
                except:
                    None

                if o!=1:

                    if o == graph[1]:
                        a=False
                        self.delete(graph)
                        self.choices()



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

    def affichage_des_rosters(self):
        # Initialisation des rosters
        num_pokemon = 5  # Modifiable
        self.roster_player1 = Roster(pokemon_df, num_pokemon)
        self.roster_player2 = Roster(pokemon_df, num_pokemon)

        # Équilibrage des équipes
        Roster.balance_rosters(self.roster_player1, self.roster_player2)

        # Affichage des rosters
        print("\nRoster joueur 1:")
        self.roster_player1.print_roster()
        print("\nRoster joueur 2:")
        self.roster_player2.print_roster()

        None






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

    def verif_morpion(self,morpion,pendule):
        en_jeu=True

        #Vérification des lignes
        for ligne in range (3):
            if morpion.casier[ligne][0].valeur == morpion.casier[ligne][1].valeur == morpion.casier[ligne][2].valeur and morpion.casier[ligne][0].valeur != 0:

                morpion.game=False
                en_jeu = False


        #Vérification des colonnes
        for colonne in range (3):
            if morpion.casier[0][colonne].valeur == morpion.casier[1][colonne].valeur == morpion.casier[2][colonne].valeur and morpion.casier[0][colonne].valeur != 0:

                morpion.game=False
                en_jeu = False


        #Vérification des diagonales
        if morpion.casier[0][0].valeur==morpion.casier[1][1].valeur==morpion.casier[2][2].valeur and morpion.casier[0][0].valeur!=0:

            morpion.game = False
            en_jeu = False


        if morpion.casier[0][2].valeur==morpion.casier[1][1].valeur==morpion.casier[2][0].valeur and morpion.casier[1][1].valeur!=0:

            morpion.game = False
            en_jeu = False

        if en_jeu is False:
            if pendule%2==0:
                morpion.valeur=1
            else:
                morpion.valeur=2

        return en_jeu



    def tour(self,pendule,z=20):
        self.choixpokemon()

        clic=g.attendreClic()
        o=g.recupererObjet(clic.x,clic.y)
        good=True

        essai=0
        while good:
            essai+=1

            if o in self.relation.keys() and o not in self.dejapris:
                a = self.relation[o]
                if pendule==0 or self.verif==False:
                    self.dejapris.append(o)

                    good=False
                else:
                    
                    if self.grille[dicrec[a[0]]].actif==1:
                        self.dejapris.append(o)

                        good=False

            else:
                clic=g.attendreClic()
                o = g.recupererObjet(clic.x, clic.y)

        print(self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur,pendule)

        if pendule%2==0:
            self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur = 1
        else:
            self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur = 2

        x=a[0][0]*X/3+a[1][0]*X/9
        y=a[0][1]*Y/3+a[1][1]*Y/9

        prochain = dicrec[a[1]]
        if self.grille[prochain].valeur==0: #Si la zone où l'on veut jouer est disponible

            #On remet l'ancienne couleur et on met la nouvelle couleure dans la zone à jouer
            if z!= 20:
                self.changement_de_couleur(dicrec[a[0]],"plum")
            self.changement_de_couleur(dicrec[a[1]],'slateblue')
            self.verif=True

            #On désactive l'ancien morpion et on active le prochain
            self.grille[dicrec[a[0]]].actif = 0
            self.grille[prochain].actif=1

        if self.grille[prochain].valeur!=0:#Si la prochaine zone à jouer n'est pas disponible
            self.changement_de_couleur(dicrec[a[0]], "plum")
            self.verif=False


        #On vérifie si le petit morpion est terminé
        if self.verif_morpion(self.grille[dicrec[a[0]]],pendule):#pas terminé
            g.changerCouleur(self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].objet, "olivedrab")

            # Affichage du sympbole du joueur si le morpion est encore en jeu
            g.afficherTexte(ref[self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur], y + Y / 18, x + X / 18,
                            'black', 30)
        else:#On donne le grand morpion à un joueur
            g.dessinerRectangle((a[0][1]*X/3)+2,(a[0][0]*Y/3)+2,(X/3)-4,(Y/3)-4,'light blue')
            g.afficherTexte(ref[self.grille[dicrec[a[0]]].valeur],(a[0][1]*Y/3)+Y/6,(a[0][0]*X/3)+X/6,"black",100)
            if self.grille[prochain].valeur!=0:

                self.verif=False

        #On remet de la couleur sur les cases déjà prise
        self.grille[dicrec[a[0]]].maj()
        self.grille[dicrec[a[1]]].maj()

        return prochain

    def jeu_en_duo(self):
        self.initgraph()
        self.remplissage()
        self.affichage_des_rosters()
        cpt = 0
        while True:
            if cpt == 0:
                ancien = self.tour(cpt)
            else:

                ancien = self.tour(cpt, ancien)
            cpt += 1

    def jeu_vs_ia(self):
        return None

    def choixpokemon(self):
        return None




poke=jeu()
poke.Menu()

g.attendreClic()
g.fermerFenetre()


