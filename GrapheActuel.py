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
    
    def __init__(self,nom: str, x: int or float , y: int or float, taille: int or float, adjacents: list):    
    #taille est une valeur entre 0 et 100 qui donne le rayon entre 10 et 50.
        self.nom = nom
        self.pos = [x,y]
        self.r = 10 + taille*25/100
        self.voisins = adjacents
        for noeud in self.voisins:
            cote = Edge(self,noeud)
            self.cotes.append(cote)
            noeud.voisins.append(self)
            Segments[str(cote.nom)] = cote
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
            Segments[make_name_from_vars([self, v], '_')] = Edge(self, v, math.sqrt((self.pos[0]-v.pos[0])**2 + (self.pos[1]-v.pos[1])**2))
      
    def __repr__(self):
        return f"{self.nom}({self.pos})"

#-----Côtés-----

class Edge:
    global Segments
    
    #Extrémités (list)
    ext = []
    
    long = 0
   
    nom = "Edge anonyme"
    
    def __init__(self,noeud1,noeud2, hypotenuse):
        self.ext = [noeud1,noeud2]
        self.long = hypotenuse
        if type(noeud1) == Noeud and type(noeud2) == Noeud:
            self.nom = noeud1.nom + '_' + noeud2.nom
        
    def __repr__(self):
       return f"{self.nom}"


#===Fonctions===

#-----Fonction d'exécution du programme-----

def execute():
    global Points, Segments, nombre_points

    while True:
        
        generePoints(nombre_points)

        trouvevoisins(Points)

        if cherche_iles(Points):
            break

    export_graphe([Points, Segments])

    Affiche(Points, Segments)

#-----Affichage de Pygame sur l'ecran-----

def Affiche(points: list, segments: list):
    global noeud1 #debug
    continuer = True
    couleur_fond = BLANC
    while continuer:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
        
        screen.fill(couleur_fond)
        for key, fig in segments.items():
            pygame.draw.line(screen, ROUGE, fig.ext[0].pos, fig.ext[1].pos, 2)
        for fig in points:
            pygame.draw.circle(screen, BLEU, fig.pos, fig.r)
            nomPoint = font.render(fig.nom, True, NOIR)
            screen.blit(nomPoint, [fig.pos[0]+fig.r,fig.pos[1]])
        
        pygame.display.flip()
        clock.tick(10)
        
    pygame.quit()

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
        voisin1 = Edge(0, 0, diagonale_plan)
        voisin2 = Edge(0, 0, diagonale_plan)
        voisin3 = Edge(0, 0, diagonale_plan)
        for j in Points:
            if i != j:
                hypotenuse = math.sqrt((i.pos[0] - j.pos[0])**2 + (i.pos[1] - j.pos[1])**2)
                if hypotenuse < voisin1.long:
                    voisin3 = voisin2
                    voisin2 = voisin1
                    voisin1 = Edge(i, j, hypotenuse)
                elif hypotenuse < voisin2.long:
                    voisin3 = voisin2
                    voisin2 = Edge(i, j, hypotenuse)
                elif hypotenuse < voisin3.long:
                    voisin3 = Edge(i, j, hypotenuse)

            
        présence1 = présence2 = présence3 = False
        sortie = 0  # Sortir de a boucle si c'est inutile de continuer
        for _, k in Segments.items():
            if k == voisin1:
                présence1 = True
                sortie += 1
            if k == voisin2:
                présence2 = True
                sortie += 1
            if k == voisin2:
                présence3 = True
                sortie += 1
            if sortie == 3: # Les trois points sont déjà présents, pas nécessaire de continuer à itérer
                break

        nom1 = make_name_from_vars([voisin1.ext[0], voisin1.ext[1]], '_')
        nom2 = make_name_from_vars([voisin2.ext[0], voisin2.ext[1]], '_')
        nom3 = make_name_from_vars([voisin3.ext[0], voisin3.ext[1]], '_')

        if présence1 == False:
            Segments[nom1] = voisin1
            voisin1.ext[0].ajoute_voisin([voisin1.ext[1]])
        
        if présence2 == False:
            Segments[nom2] = voisin2
            voisin2.ext[0].ajoute_voisin([voisin2.ext[1]])
                
        if présence3 == False:
            Segments[nom3] = voisin3
            voisin3.ext[0].ajoute_voisin([voisin3.ext[1]])
 
    for key in list(Segments):
        Segments.pop(key)
        break


# Vérifie si tous les points sont reliés. Choisit un point, puis ses voisins, puis les voisins de voisins etc. et regarde si tous les points sont dedans.
def cherche_iles(noeuds: list):
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
    for key, segment in Graphe[1].items():
        declaration = f'Edge({segment.ext[0]}, {segment.ext[1]}, {segment.long})'
        content += declaration + '\n'
    with open('Graphe_File.txt', 'w') as file:
        file.write(content)
 
#-----Créer des noms sous forme de str à partir de variables-----

def make_name_from_vars(vars: list, separator: str):    # Utile p. ex. pour donner des noms aux éléments de dictionnaires, comme 'Segments'
    name = ''
    for index, elmt in enumerate(vars):
        name += str(elmt.nom)
        if index < len(vars) - 1:
            name += separator
    return name


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
Segments = {}
nombre_points = 20

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
    
execute()