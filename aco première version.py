#===Imports===

import pygame
import math
import random
import time


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
    
    def __init__(self,nom: str, x: int or float , y: int or float, taille: int or float, adjacents: list):    
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

    def ajoute_voisin(self, liste: list):
        # if self in liste: return      # À quoi sert cette ligne ? CV
        if self in liste:
            liste.pop(liste.index(self))    # On enlève 'self' des voisins à ajouter
        global Segments
        for i in liste:
            if i in self.voisins:
                liste.pop(liste.index(i))   # On enlève de 'liste' les voisins déjà existants
        self.voisins += liste
        for v in liste:
            v.voisins.append(self)
            Segments.append(Vertice(self, v, math.sqrt((self.pos[0]-v.pos[0])**2 + (self.pos[1]-v.pos[1])**2), 10))
      
    def __repr__(self):
        return f"{self.nom}({self.pos})"

#-----Côtés-----

class Vertice:
    global Segments
    
    #Extrémités (list)
    ext = []
    
    long = 0
   
    nom = "vertice anonyme"
    
    fer = 10
    
    def __init__(self,noeud1,noeud2, hypotenuse, feromone):
        self.ext = [noeud1,noeud2]
        self.long = hypotenuse
        self.fer = feromone
        if type(noeud1) == Noeud and type(noeud2) == Noeud:
            self.nom = noeud1.nom + '_' + noeud2.nom
        
    def __repr__(self):
       return f"{self.nom}"
    
#-----Fourmis-----
    
class Fourmis:
    global Points
    
    nom = ""
    
    pos = []
    
    point = 0
    
    chem = []
    
    def __init__(self,nom , pos, Points, chemin):
        self.nom = nom
        self.pos = pos
        self.point = Points
        self.chem = chemin
        
    def __repr__(self):
       return f"{self.nom, self.pos}"
        
#===Fonctions===

#-----fonctionnement des fourmis-----
def cree_fourmis(nombre: int):
    global Points, listfourmis
    
    listfourmis = []
    for i in range (0, nombre):
        listfourmis.append(Fourmis("F"+str(i), Points[0].pos, Points[0], []))
       
def mouve_fourmis():
    global Segments, listfourmis, Points
     
    for i in listfourmis:
        voisins = []
        somme_fer = 0
        index = 0
        for j in Segments:
            if j.ext[0] == i.point:
                somme_fer += j.fer
                for k in range(0, j.fer):
                    voisins.append(j)
        
        i.chem.append(j)
        index = voisins[random.randint(0, somme_fer - 1)].ext[1]
        i.pos = index.pos
        i.point = index
        #print(voisins[random.randint(0, somme_fer - 1)].pos)


#-----Fonction d'exécution du programme-----

def execute():
    global Points, Segments, nombre_points

    while True:
        
        generePoints(nombre_points)

        trouvevoisins(Points)

        if cherche_iles(Points):
            break
    cree_fourmis(5)
    
    export_graphe([Points, Segments])
    
    #print(Points[0].voisins)
    
    frame = 0
    continuer = True
    while continuer:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            
        frame += 1
        Affiche(Points, Segments, listfourmis)
            
        if frame % 10 == 0:
            mouve_fourmis()
            
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

#-----Affichage de Pygame sur l'ecran-----

def Affiche(points: list, segments: list, lisfourmis: list):
    global noeud1 #debug
    couleur_fond = BLANC
        
    screen.fill(couleur_fond)
    for fig in segments:
        pygame.draw.line(screen, ROUGE, fig.ext[0].pos, fig.ext[1].pos, 2)
    for fig in points:
        pygame.draw.circle(screen, BLEU, fig.pos, fig.r)
        nomPoint = font.render(fig.nom, True, NOIR)
        screen.blit(nomPoint, [fig.pos[0]+fig.r,fig.pos[1]])
    for fig in listfourmis:
        pygame.draw.circle(screen, JAUNE, fig.pos, 3)
        

#-----Génération de points-----

def generePoints(nombre: int):
    global Points, taille
    for i in range (nombre):
        x = random.randint(10,taille[0]-10)
        y = random.randint(10,taille[1]-10)
        point = Noeud("P"+str(i),x,y,-20,[])


       
def trouvevoisins(Points: list):
    global Segments
    diagonale_plan = math.sqrt(taille[0]**2 + taille[1]**2)
    for i in Points:
        voisin1 = Vertice(0, 0, diagonale_plan, 10)
        voisin2 = Vertice(0, 0, diagonale_plan, 10)
        voisin3 = Vertice(0, 0, diagonale_plan, 10)
        for j in Points:
            if i != j:
                hypotenuse = math.sqrt((i.pos[0] - j.pos[0])**2 + (i.pos[1] - j.pos[1])**2)
                if hypotenuse < voisin1.long:
                    voisin3 = voisin2
                    voisin2 = voisin1
                    voisin1 = Vertice(i, j, hypotenuse, 10)
                elif hypotenuse < voisin2.long:
                    voisin3 = voisin2
                    voisin2 = Vertice(i, j, hypotenuse, 10)
                elif hypotenuse < voisin3.long:
                    voisin3 = Vertice(i, j, hypotenuse, 10)

            
        présence1 = présence2 = présence3 = False
        sortie = 0  # Sortir de a boucle si c'est inutile de continuer
        for k in Segments:
            if k == voisin1:
                présence1 = True
                sortie += 1
            if k == voisin2:
                présence2 = True
                sortie += 1
            if k == voisin3:
                présence3 = True
                sortie += 1
            if sortie == 3: # Les trois points sont déjà présents, pas nécessaire de continuer à itérer
                break

        if présence1 == False:
            Segments.append(voisin1)
            voisin1.ext[0].ajoute_voisin([voisin1.ext[1]])
        
        if présence2 == False:
            Segments.append(voisin2)
            voisin2.ext[0].ajoute_voisin([voisin2.ext[1]])
                
        if présence3 == False:
            Segments.append(voisin3)
            voisin3.ext[0].ajoute_voisin([voisin3.ext[1]])
    
    element = 0
    for a in Segments:
        for z in Segments:
            if a == z:
                del(Segments[element])
                break
        element += 1

def cherche_iles(noeuds: list): # Vérifie si tous les points sont reliés. Choisit un point, puis ses voisins, puis les voisins de voisins etc. et regarde si tous les points sont dedans.
    reseau = noeuds[0].voisins # Réseau de points liés, liste
    for v in reseau:
        for elmt in v.voisins:  # elmt est voisin d'un point de 'reseau'     elmt pour 'élément' si jamais
            if elmt not in reseau:
                reseau.append(elmt)
    if len(reseau) == len(noeuds):  # S'il y a tous les points du graphe dans 'reseau' c'est bon --> True
        return True
    else: return False

#-----Création d'un document txt contenant le graphe-----

def export_graphe(Graphe: list):  # Graphe = [Points, Segments]
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
nombre_points = 8

#-----Affichage-----

taille = (700, 400)


#===Exécution===

pygame.init()
pygame.display.set_caption(' Graphe')
screen = pygame.display.set_mode(taille)
clock = pygame.time.Clock()

#-----Texte-----
    
font = pygame.font.SysFont('Arial', 24, True, False)

#-----Affichage-----
    
execute()
