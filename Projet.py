from tkiteasy import *
import numpy as np
X,Y=800,800
g=ouvrirFenetre(X,Y)


dic={0:(0,0),1:(0,1),2:(0,2),3:(1,0),4:(1,1),5:(1,2),6:(2,0),7:(2,1),8:(2,2)}
dicrec={(0,0):0,(0,1):1,(0,2):2,(1,0):3,(1,1):4,(1,2):5,(2,0):6,(2,1):7,(2,2):8}

ref={0:"",1:"x",2:"o"}

def positionin(x,y,a,b,c,d):
    if x>a and x<c and y>b and y<d:
        return True
    return False
class Morpion() :
    def __init__(self,k):
        self.plateau=np.full((3,3),0)
        self.game=True
        self.numero=k

    def ajoutcase(self,k):
        self.casier=[]
        # On rajoute les 9 cases du morpion
        for i in range(3):
            ligne = []
            for j in range(3):
                x=k[0]*3+i
                y=k[1]*3+j

                ligne.append(Case(k,(i,j),poke.tabgraph[x][y]))
                poke.relation[poke.tabgraph[x][y]]=(k,(i,j))
                if j==2:

                    self.casier.append(ligne)


    def tour(self):
        self.plateau[1,0]=1
        return None

class Case():
    def __init__(self,k,tu,objet):
        self.indice=(k,tu)
        self.valeur=0
        self.objet=objet


    def changement_de_valeur(self):
        return None

class jeu():
    def __init__(self):
        self.grille=[]
        for i in range (10):
            self.grille.append(Morpion(i))
        self.relation={}
        self.dejapris=[]

    def initgraph(self):
        self.tabgraph=[]

        for i in range (9):
            tab=[]
            for j in range (9):
                rect=g.dessinerRectangle(j*X/9,i*Y/9,X/9,(Y/9)-1,'blue')

                tab.append(rect)
                if j ==8:

                    self.tabgraph.append(tab)
        g.changerCouleur(self.tabgraph[4][0],'red')
        a=self.tabgraph[0][0]
        g.changerCouleur(a,"purple")



        for i in range (1,10):
            couleur = 'white'
            ep=1
            if i%3==0:
                couleur="red"
                ep=4


            g.dessinerLigne(i*X/9,0,i*X/9,Y,couleur,ep=ep)
            g.dessinerLigne(0,i*Y/9,X,i*Y/9,couleur,ep=ep)



    def remplissage(self): #Pour chaque morpion, on lui rajoute ses cases
        i=0
        for m in self.grille:
            m.ajoutcase(dic[i])
            i+=1
            if i ==9:
                break


    def changement_de_couleur(self,k):
        for i in range (3):

            for j in range(3):
                g.changerCouleur(self.grille[k].casier[i][j].objet,'light green')

    def tour(self,p):
        clic=g.attendreClic()
        o=g.recupererObjet(clic.x,clic.y)
        good=True

        while good:
            if o in self.relation.keys() and o not in self.dejapris:
                self.dejapris.append(o)
                a = self.relation[o]
                good=False
            else:
                clic=g.attendreClic()
                o = g.recupererObjet(clic.x, clic.y)

        if p%2==0:
            self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur=1
        else:
            self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur = 2

        x=a[0][0]*X/3+a[1][0]*X/9
        y=a[0][1]*Y/3+a[1][1]*Y/9


        g.changerCouleur(self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].objet,"orange")

        #Affichage du sympbole du joueur
        g.afficherTexte(ref[self.grille[dicrec[a[0]]].casier[a[1][0]][a[1][1]].valeur],y+Y/18,x+X/18,'black',20)


poke=jeu()
poke.initgraph()

poke.remplissage()
poke.changement_de_couleur(5)
g.changerCouleur(poke.tabgraph[7][0],"red")
cpt=0
while True:

    poke.tour(cpt)
    cpt+=1
g.attendreClic()
g.fermerFenetre()
