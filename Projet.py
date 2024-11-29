from tkiteasy import *
import numpy as np
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

def positionin(x,y,a,b,c,d):
    if x>a and x<c and y>b and y<d:
        return True
    return False
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
        text = [g.afficherTexte("Bienvenue dans le jeu Poke-Tac-Toe", GX / 2, 2 * GY / 5, "Black", int(GX / 22)),
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
        graph = [g.afficherImage(GX/6,0.5*GY,"1 vs 1.png"),g.afficherImage(0.6*GX,0.5*GY-20,"Mode IA.png")]


        while a:

            clic = g.attendreClic()
            o = g.recupererObjet(clic.x, clic.y)

            if o in graph:
                self.delete(graph)
                a = False
            if o == graph[0]:
                self.jeu_en_duo()
            if o == graph[1]:
                self.jeu_vs_ia()
            if o == graph[2]:
                self.choices2()
            if o == graph[3]:
                self.settings()
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

        clic=g.attendreClic()
        o=g.recupererObjet(clic.x,clic.y)
        good=True

        while good:

            if o in self.relation.keys() and o not in self.dejapris:
                self.dejapris.append(o)
                a = self.relation[o]
                if pendule==0 or self.verif==False:
                    good=False
                else:
                    
                    if self.grille[dicrec[a[0]]].actif==1:
                        good=False

            else:
                clic=g.attendreClic()
                o = g.recupererObjet(clic.x, clic.y)



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


        #On vérifie si le petit morpion est terminé
        if self.verif_morpion(self.grille[dicrec[a[0]]],pendule):
            g.changerCouleur(self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].objet, "olivedrab")

            # Affichage du sympbole du joueur
            g.afficherTexte(ref[self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur], y + Y / 18, x + X / 18,
                            'black', 30)
        else:
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




poke=jeu()
poke.Menu()



g.attendreClic()
g.fermerFenetre()


