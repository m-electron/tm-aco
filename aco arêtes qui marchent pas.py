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

    def ajoute_voisin(self, liste):  # Modif CV
        if self in liste: return
        global Segments
        for i in liste:
            if i in self.voisins:
                liste.pop(liste.index(i))
        self.voisins += liste
        for v in liste:
            if v not in Segments:
                Segments.append(Vertice(self, v, math.sqrt((self.pos[0]-v.pos[0])**2 + (self.pos[1]-v.pos[1])**2))) # Modif CV
      
    def __repr__(self):
        return f"{self.nom}({self.pos})"

#-----Côtés-----

class Vertice:
    global Segments
    
    #Extrémités (list)
    ext = []
    
    long = 0
   
    nom = "vertice anonyme"
    
    def __init__(self,noeud1,noeud2, hypotenuse):
        self.ext = [noeud1,noeud2]
        self.long = hypotenuse
        if type(noeud1) == Noeud and type(noeud2) == Noeud:
            self.nom = noeud1.nom + '_' + noeud2.nom
        
    def __repr__(self):
       return f"{self.nom}"


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
            pygame.draw.line(screen, ROUGE, fig.ext[0].pos, fig.ext[1].pos, 2)
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
    global Points, nombre, Segments
    for i in Points:
        diagonale_plan = math.sqrt(taille[0]**2 + taille[1]**2)
        voisin1 = Vertice(0, 0, diagonale_plan)
        voisin2 = Vertice(0, 0, diagonale_plan)
        voisin3 = Vertice(0, 0, diagonale_plan)
        for j in Points:
            if i != j:
                hypotenuse = math.sqrt((i.pos[0] - j.pos[0])**2 + (i.pos[1] - j.pos[1])**2)
                if hypotenuse < voisin1.long:
                    voisin2 = voisin1
                    voisin3 = voisin2
                    voisin1 = Vertice(i, j, hypotenuse)
                elif hypotenuse < voisin2.long:
                    voisin3 = voisin2
                    voisin2 = Vertice(i, j, hypotenuse)
                elif hypotenuse < voisin3.long:
                    voisin3 = Vertice(i, j, hypotenuse)

            
        présence =  False
        for k in Segments:
            if k == voisin1:
                présence = True
                break
        if présence == False:
            Segments.append(voisin1)
            voisin1.ext[0].ajoute_voisin([voisin1.ext[1]])
                
        présence =  False
        for k in Segments:
            if k == voisin2:
                présence = True
                break
        if présence == False:
            Segments.append(voisin2)
            voisin2.ext[0].ajoute_voisin([voisin2.ext[1]])
                
        présence =  False
        for k in Segments:
            if k == voisin3:
                présence = True
                break
        if présence == False:
            Segments.append(voisin3)
            voisin3.ext[0].ajoute_voisin([voisin3.ext[1]])
 
    Segments.pop(0)

#-----Création d'un document txt contenant le graphe-----

def export_graphe(Graphe):  # Graphe = [Points, Segments]
    content = ''
    for point in Graphe[0]:
        declaration = f'Noeud({point.nom}, {point.pos[0]}, {point.pos[1]}, {(point.r - 10)*4}, {point.voisins})'
        content += declaration + '\n'
    for segment in Graphe[1]:
        declaration = f'Vertice({segment.ext[0]}, {segment.ext[1]}, {segment.long})'
        content += declaration + '\n'
    with open('Graphe_File.txt', 'w') as file:
        file.write(content)
 
 
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

trouvevoisins()

export_graphe([Points, Segments])

Affiche(Points,Segments)
