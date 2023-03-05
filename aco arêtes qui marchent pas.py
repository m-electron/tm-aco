#===Imports===

import pygame
import math
import random


#===Classes===

#-----Noeuds-----

class Noeud:
   global Points
   
   nom = ""
   
   #Position)
   pos = []
   r = 0
   
   #Voisins
   voisins = []
   
   #Côtés
   cotes = []
    
   def __init__(self,nom,x,y,taille,adjacents):    
   #taille est une valeur entre 0 et 100 qui donne le rayon entre 10 et 50.
        self.nom = nom
        self.pos = [x,y]
        self.r = 10 + taille*25/100
        self.voisins = adjacents
        for noeud in self.voisins:
            cote = Vertice(self,noeud)
            self.cotes.append(cote)
            noeud.voisins.append(self)
            Segments.append(cote)
        Points.append(self)     

   def __repr__(self):
        affiche_voisins = ""
        i = 0    #index pour l'affichage des virgules entre les voisins
        for v in self.voisins:
            affiche_voisins += str(v.pos)
            i += 1
            if i < len(self.voisins):
                affiche_voisins += ', '
        return f"{self.nom}({self.pos})"

#-----Côtés-----

class Vertice:
    global Segments
    
    #Extrémités (list)
    ext = []
    
    long = 0
    
    def __init__(self,noeud1,noeud2):
        self.ext = [noeud1,noeud2]
        self.long = math.sqrt((self.ext[0].pos[0]-self.ext[1].pos[0])**2 + (self.ext[0].pos[1]-self.ext[1].pos[1])**2)
        
    def __repr__(self):
        return f"|Vertice| Extrémités : {self.ext[0]}, {self.ext[1]}"


#===Fonctions===

#-----Affichage de Pygame sur l'ecran-----

def Affiche(points,segments):
    global noeud1 #debug
    continuer = True
    couleur_fond = BLANC
    while continuer:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
        
        screen.fill(couleur_fond)
        for fig in segments:
            pygame.draw.line(screen, ROUGE, fig.ext[0].pos, fig.ext[1].pos, 7)
            longueur = font.render(str(int(fig.long)), True, NOIR)
            screen.blit(longueur, [(fig.ext[0].pos[0]+fig.ext[1].pos[0])/2,(fig.ext[0].pos[1]+fig.ext[1].pos[1])/2])
        for fig in points:
            pygame.draw.circle(screen, BLEU, fig.pos, fig.r)
            nomPoint = font.render(fig.nom, True, NOIR)
            screen.blit(nomPoint, [fig.pos[0]+fig.r,fig.pos[1]])
        
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

#-----Génération de points-----

def generePoints(nombre):
    global Points, taille
    for i in range (nombre):
        x = random.randint(10,taille[0]-10)
        y = random.randint(10,taille[1]-10)
        """voisins = []
        n = random.randint(1,len(Points))
        
        
        for v in range(len(Points)):
            if random.randint(0,1):
                voisins.append()"""
        point = Noeud("P"+str(i),x,y,-20,[])


       
def trouvevoisins():
    global taille, Points, nombre
    voisin1 = (1000, 0, 0)
    voisin2 = (1000, 0, 0)
    voisin3 = (1000, 0, 0)
    for i in Points:
        for j in Points:
            if i != j:
                hypotenuse = math.sqrt((i.pos[0] - j.pos[0])**2 + (i.pos[1] - j.pos[1])**2)
                if hypotenuse < voisin1[0]:
                    voisin2 = voisin1
                    voisin3 = voisin2
                    voisin1 = (hypotenuse, i, j)
                elif hypotenuse < voisin2[0]:
                    voisin3 = voisin2
                    voisin2 = (hypotenuse, i, j)
                elif hypotenuse < voisin3[0]:
                    voisin3 = (hypotenuse, i, j)
                    
        print((voisin1[1].pos[0], voisin1[1].pos[1]))
        print((voisin1[2].pos[0], voisin1[2].pos[1]))
        
        pygame.draw.line(screen, ROUGE, (50, 200), (500, 700), 5)
        
        pygame.draw.line(screen, ROUGE, [voisin1[1].pos[0], voisin1[1].pos[1]], [voisin1[2].pos[0], voisin1[2].pos[1]])
        #pygame.draw.line(screen, ROUGE, voisin2[1].pos, voisin2[2].pos)
        #pygame.draw.line(screen, ROUGE, voisin3[1].pos, voisin3[2].pos)


#===Constantes couleurs===

BLANC = (255,255,255)
NOIR = (0,0,0)
GRIS = (215, 219, 216)
ROUGE = (255,0,0)
VERT = (0,255,0)
BLEU = (0,0,255)
JAUNE = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
VERTFONCE = (48,162,38) 
ORANGE = (199,95,48)


#===Variables===

#-----Graphe-----

Points = []
Segments = []

#-----Affichage-----

taille = (1000, 700)


#===Exécution===

pygame.init()
pygame.display.set_caption(' Graphe')
screen = pygame.display.set_mode(taille)
clock = pygame.time.Clock()

#-----Texte-----
    
font = pygame.font.SysFont('Arial', 24, True, False)

#-----Affichage-----

#trouvevoisins()
    
generePoints(20)

Affiche(Points,Segments)

trouvevoisins()
    