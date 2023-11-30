#===Imports===

import pygame
import math
import random
import csv
import time

#===Classes===

#-----Noeuds-----

class Noeud:
    global Points
   
    nom = ""
   
    #Position)
    pos = []
    r = 0
   
    #jsp pourquoi c'est là mais ça marche
    voisins = []
    
    #Segments adjacents
    seg = []

    def __init__(self,nom: str, x: int or float , y: int or float, taille: int or float, adjacents: list, segments: list):    
    #taille est une valeur entre 0 et 100 qui donne le rayon entre 10 et 50.
        global Segments
        self.nom = nom
        self.pos = [x,y]
        self.r = 10 + taille*25/100
        self.voisins = adjacents
        self.seg = segments


        for noeud in self.voisins:
            cote = Arete(self,noeud)
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
            Segments.append(Arete(self, v, math.sqrt((self.pos[0]-v.pos[0])**2 + (self.pos[1]-v.pos[1])**2), 10))
            
      
    def __repr__(self):
        return f"{self.nom}({self.pos})"

#-----Côtés-----

class Arete:
    global Segments
    
    #Extrémités (list)
    ext = []
    
    long = 0
   
    nom = "Arete anonyme"
    
    fer = 10
    
    def __init__(self,noeud1,noeud2, hypotenuse, feromone: int):
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
    
    distance = 0
    
    p_visité = []
    
    def __init__(self,nom , pos, Points, chemin, points : list):
        self.nom = nom
        self.pos = pos
        self.point = Points
        self.chem = chemin
        self.p_visité = points

        
    def __repr__(self):
       return f"{self.nom, self.pos}"
        
#===Fonctions===

#-----fonctionnement des fourmis-----
def cree_fourmis(nombre: int):
    global Points, listfourmis
    
    listfourmis = []
    for i in range (0, nombre):
        listfourmis.append(Fourmis("F"+str(i), Points[0].pos, Points[0], [], [Points[0]]))
      
def mouve_fourmis():
    global Segments, listfourmis, Points, nombre_fourmis, fin, chem_possible
    
    
    for i in listfourmis:
        
        
        if i.distance == 0:
            
            i.point.r -= 20 / nombre_fourmis 
            Points[0].r = 5
            #print(len(i.p_visité))
            
            if len(i.p_visité) == len(Points):
                
                longeur_chemin = 0
                somme_fer = 0
                for h in i.chem:
                    longeur_chemin += h.long
                for h in i.chem:
                    #h.fer += ((math.sqrt(taille[0]^2 + taille[1]^2) + 10000) / (0.1 * longeur_chemin * h.long))
                    h.fer += 110000 / longeur_chemin / h.long
                    somme_fer += h.fer
                #print(somme_fer)
                #print(".")
                

                if i.chem not in chem_possible:
                    chem_possible.append(i.chem)
                

                i.chem = []
                i.pos = Points[0].pos
                i.point = Points[0]
                i.p_visité = []
                
           
            else:
                somme_fer = 0
                liste_segments = []
                for j in i.point.seg:

                    if j.ext[0] == i.point:
                        if j.ext[1] not in i.p_visité:
                            somme_fer += j.fer
                            liste_segments.append((somme_fer, j))
                            
                    if j.ext[1] == i.point:
                        if j.ext[0] not in i.p_visité:
                            somme_fer += j.fer
                            liste_segments.append((somme_fer, j))

                nombre_alea = 0
                nombre_alea = random.uniform(0, somme_fer - 1)
                seg_emprunté = Segments[0]
                
                
                #print(liste_segments)
                
                for k in liste_segments:
                    if nombre_alea < k[0]:
                        seg_emprunté = k[1]
                        break
                
                i.distance += int(seg_emprunté.long / 10)
                
                if seg_emprunté.ext[0] == i.point:
                    if seg_emprunté.ext[1] == Points[0]:
                        i.chem = []
                        i.p_visité = []
                        
                    i.chem.append(seg_emprunté)
                    i.pos = seg_emprunté.ext[1].pos
                    i.point = seg_emprunté.ext[1]
                    i.p_visité.append(seg_emprunté.ext[1])
                    seg_emprunté.ext[1].r += 20 / nombre_fourmis
                    
                elif seg_emprunté.ext[1] == i.point:
                    if seg_emprunté.ext[0] == Points[0]:
                        i.chem = []
                        i.p_visité = []
                        
                    i.chem.append(seg_emprunté)
                    i.pos = seg_emprunté.ext[0].pos
                    i.point = seg_emprunté.ext[0]
                    i.p_visité.append(seg_emprunté.ext[0])
                    seg_emprunté.ext[0].r += 20 / nombre_fourmis
                
                else:
                    i.pos = Points[0].pos
                    i.point = Points[0]
                    i.chem = []
                    i.p_visité = []
        else:
            i.distance -= 1


def best_chemin():
    global Points, Segments, fin, best_chem, nombre_points
    
    fin = False
    
    best_chem = [] 
    noeud = Points[0]
    point_visité = [Points[0]]
    seg_emprunté = []
    longeur = 0
    
    while len(point_visité) != len(Points):
        best_seg = (0, 0)
        if type(noeud) == Arete:
            pass
        for i in noeud.seg:
            if noeud == i.ext[0]:
                if i.ext[1] not in point_visité and i not in seg_emprunté:
                    if i.fer > best_seg[0]:
                        best_seg = (i.fer, i)
            else:
                if i.ext[0] not in point_visité and i not in seg_emprunté:
                    if i.fer > best_seg[0]:
                        best_seg = (i.fer, i)
                        
        if best_seg == (0, 0):
            noeud = point_visité[-2]
            best_chem.pop()
            point_visité.pop()
            
        else:            
            best_chem.append(best_seg[1])
            
            if noeud == best_seg[1].ext[0]:
                noeud = best_seg[1].ext[1]
                point_visité.append(noeud)
            else:
                noeud = best_seg[1].ext[0]
                point_visité.append(noeud)
        
        seg_emprunté.append(best_seg)
            
        if len(seg_emprunté) > 2:
            seg_emprunté.remove(seg_emprunté[0])
            
    for i in best_chem:
        longeur += i.long
        
    print(longeur)
    
    
def reinitialisation():
    global Points, Segments, listfourmis, fin
    
    for i in Points:
        i.r = 5
    for j in Segments:
        j.fer = 10
    for k in listfourmis:
        k.pos = Points[0].pos
        k.point = Points[0]
        k.chem = []
        k.distance = 0
        k.p_visité = [Points[0]]
    fin = True
    
#-----Fonction d'exécution du programme-----

def execute():
    global Points, Segments, nombre_points, listfourmis, fin, nombre_iteration

    if mode_copie != 'copie':
        while True:

            generePoints(nombre_points)

            trouvevoisins(Points)


            if cherche_iles(Points):
                break

            Points = []
            Segments = []

    else:
        copie_graphe([], [], 'copie', adresse)
    print('copié')
        
    cree_fourmis(nombre_fourmis)
    print('fourmis')
    
    nettoyer_segment()
    print('nettoyé')
    
        
    Segments_adjacents()
    print('adjacents')
    cree_fourmis(nombre_fourmis)
    
    print(listfourmis[0].point.seg[0].ext[1] == listfourmis[0].point)
    #code pour avoir directement la solution----------------
    for i in range(1, nombre_iteration):
        t0 = time.time()
        while fin:
            mouve_fourmis()
            if time.time() - t0 > 2:
                best_chemin()
        print(i, "/"*10)
        
        if i != nombre_iteration - 1:
            reinitialisation()
    #-------------------------------------------------------
    """
    chem_court = 10000
    
    for i in chem_possible:
        long = 0
        for j in i:
            long += j.long
        if long < chem_court:
            chem_court = long
    
    print(chem_court)
    """
    
    frame = 0
    continuer = True
    cnt = 2
    while continuer:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            
        frame += 1
        Affiche(Points, Segments, listfourmis)
        
        # code pour voir l'affichage --------------------------
        """
        if fin:    
            if frame % 1 == 0:
                mouve_fourmis()
                for seg in Segments:
                    if seg.fer > 200:
                        best_chemin()
        """
        #---------------------------------------------------

        pygame.display.flip()
        clock.tick(10)
        cnt -= 1
        
    pygame.quit()

#-----Affichage de Pygame sur l'ecran-----

def Affiche(points: list, segments: list, lisfourmis: list):
    global noeud1, best_chem #debug
    couleur_fond = BLANC
        
    screen.fill(couleur_fond)
    for fig in segments:
        couleur = fig.fer
        if couleur > 255:
            couleur = 255
        pygame.draw.line(screen, (255, couleur, 0), fig.ext[0].pos, fig.ext[1].pos, 2)
    for fig in points:
        pygame.draw.circle(screen, BLEU, fig.pos, fig.r)
        nomPoint = font.render(fig.nom, True, NOIR)
        screen.blit(nomPoint, [fig.pos[0],fig.pos[1]])
    for fig in listfourmis:
        pygame.draw.circle(screen, JAUNE, fig.pos, 3)
        
    if not fin:
        for fig in best_chem:
            pygame.draw.line(screen, (255, 0, 255), fig.ext[0].pos, fig.ext[1].pos, 2)
       

#-----Génération de points-----

def generePoints(nombre: int):
    global Points, taille
    for i in range (nombre):
        x = random.randint(10,taille[0]-10)
        y = random.randint(10,taille[1]-10)
        point = Noeud("P"+str(i),x,y,-20,[],[])


       
def trouvevoisins(Points: list):
    global Segments
    diagonale_plan = math.sqrt(taille[0]**2 + taille[1]**2)
    for i in Points:
        voisin1 = Arete(0, 0, diagonale_plan, 10)
        voisin2 = Arete(0, 0, diagonale_plan, 10)
        voisin3 = Arete(0, 0, diagonale_plan, 10)
        for j in Points:
            if i != j:
                hypotenuse = math.sqrt((i.pos[0] - j.pos[0])**2 + (i.pos[1] - j.pos[1])**2)
                if hypotenuse < voisin1.long:
                    voisin3 = voisin2
                    voisin2 = voisin1
                    voisin1 = Arete(i, j, hypotenuse, 10)
                elif hypotenuse < voisin2.long:
                    voisin3 = voisin2
                    voisin2 = Arete(i, j, hypotenuse, 10)
                elif hypotenuse < voisin3.long:
                    voisin3 = Arete(i, j, hypotenuse, 10)

            
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


def nettoyer_segment():
    global Segments
    for i in Segments:
        for j in Segments:
            if i.ext[0] == j.ext[1] and i.ext[1] == j.ext[0]:
                Segments.remove(j)


def Segments_adjacents():
    global Segments, Points
    for l in Points:
        for m in Segments:
            if l in m.ext:
                l.seg.append(m)


def copie_graphe(liste_points: list, liste_aretes: list, mode: str, adresse = 'Graphe_File.csv'):    # mode: 'sauvegarde'/'copie'

    if mode == 'sauvegarde':
        texte = []
        for point in liste_points:
            texte.append(['P', point.nom, point.pos, point.r, []])
        for key in liste_aretes:
            texte.append(['A', key.ext, key.long])

        with open(adresse, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['SEP=,'])    # Permet d'ouvrir le fichier csv dans excel en séparant les données en colonnes
            for row in texte:
                writer.writerow(row)

    elif mode == 'copie':
        global Points, Segments, trajet

        Points = []
        Segments = []

        with open(adresse, 'r') as f:
            texte = list(csv.reader(f, delimiter=","))

        index = 0
        for line in texte:
            match line[0]:
                case 'P':
                    Points.append(Noeud(line[1], eval(line[2])[0], eval(line[2])[1], int(line[3])+2, [], []))
                    Points.pop()
                    index = int(line[1].replace('P',''))
                case 'A':
                    ext = list(line[1][1:-1].split(', '))
                    name = str(ext[0]) + '_' + str(ext[1])
                    point_numbers = [int(ext[0].replace('P', '')), int(ext[1].replace('P', ''))]
                    Segments.append(Arete(Points[point_numbers[0]], Points[point_numbers[1]], eval(line[2]), 10))
                    Points[point_numbers[0]].voisins.append(Points[point_numbers[1]])
                    Points[point_numbers[1]].voisins.append(Points[point_numbers[0]])
    pass

 
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
nombre_points = 11
nombre_fourmis = 10
chem_possible = []
fin = True
nombre_iteration = 1
mode_copie = 'copie'    # 'copie' signifie que le graphe est copié depuis le fichier de sauvegarde du graphe
adresse = 'Graphe10.csv'

#-----Affichage-----

taille = (1000, 600)


#===Exécution===

pygame.init()
pygame.display.set_caption(' Graphe')
screen = pygame.display.set_mode(taille)
clock = pygame.time.Clock()

#-----Texte-----
    
font = pygame.font.SysFont('Times New Roman', 15, True, False)

#-----Affichage-----
    
execute()