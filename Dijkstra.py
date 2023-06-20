#===Imports===

import pygame, math, random, time

#===Classes===

#-----Noeuds-----

class Noeud:
    global Points

    nom = ""

    # Position)
    pos = []
    r = 0

    # Voisins
    voisins = []

    # Côtés
    cotes = []  # Est-ce qu'on utilise encore ça ?

    def __init__(self, nom: str, x: int or float, y: int or float, taille: int or float, adjacents: list):
        # taille est une valeur entre 0 et 100 qui donne le rayon entre 10 et 50.
        self.nom = nom
        self.pos = [x, y]
        self.r = taille
        self.voisins = adjacents
        for noeud in self.voisins:
            cote = Edge(self, noeud, pythagore(self, noeud))
            self.cotes.append(cote)
            noeud.voisins.append(self)
            Segments[str(cote.nom)] = cote
        Points.append(self)

    def ajoute_voisin(self, liste: list):
        # liste contient les voisins à ajouter. Il faut enlever les voisins déjà existants et le point lui-même
        if self in liste:
            # On enlève 'self' des voisins à ajouter
            liste.pop(liste.index(self))
        global Segments
        for i in liste:
            if i in self.voisins:
                # On enlève de 'liste' les voisins déjà existants
                liste.pop(liste.index(i))
        self.voisins += liste
        for v in liste:
            v.voisins.append(self)
            Segments[make_name_from_vars([self, v], '_')] = Edge(self, v, pythagore(self, v))

    def __repr__(self):
        return self.nom   # f"{self.nom}({self.pos})"

#-----Côtés-----

class Edge:
    global Segments

    # Extrémités (list)
    ext = []

    long = 0

    nom = "Edge anonyme"

    def __init__(self, noeud1, noeud2, hypotenuse):
        self.ext = [noeud1, noeud2]
        self.long = hypotenuse
        if type(noeud1) == Noeud and type(noeud2) == Noeud:
            self.nom = noeud1.nom + '_' + noeud2.nom

    def __repr__(self):
        return f"{self.nom}"

#-----Chemins-----

class path:
    trajet = [] # Contient les points visités dans l'ordre depuis le départ
    long = 0    # Longueur totale du trajet

    def __init__(self, points: list):
        self.trajet = points   # Le trajet commence au point de départ
        long = 0
        for i, _ in enumerate(points):
            if i == len(points)-1: break
            long += longueur_segment(points[i], points[i+1])
        self.long = long
        
    def add_point(self, point):
        self.long += longueur_segment(self.trajet[-1], point)
        self.trajet.append(point)
    
    def __repr__(self):
        return make_name_from_vars([self.trajet[0], self.trajet[-1]], '_')


# ===Fonctions===

def Dijkstra(start: Noeud, target: Noeud):

    global shortest_path
    
    resolus = {start: (0, start)}    # Points dont on connais la distance la plus courte depuis start
    candidats = {}  # Points dont on connais une distance qui n'est pas forcément la plus courte
    
    pt = start
    long = 0
    closest_point = None
    
    while True:
        for v in pt.voisins:
            long = resolus[pt][0]
            if v in resolus.keys():
                continue
            
            if v in candidats.keys() and candidats[v][0] < long + pythagore(v, pt):
                continue

            candidats[v] = (long + pythagore(v, pt), pt) # Si v déjà dans candidat, modifier la valeur longueur de v et son prédécesseur
            
        closest_point = [i for i in candidats.keys() if candidats[i][0] == min(k[0] for k in candidats.values())]
        resolus[closest_point[0]] = candidats[closest_point[0]]
        candidats.pop(closest_point[0])
        pt = closest_point[0]

        if target in resolus.keys():
            print('Trajet optimal trouvé : ', end = '')

            route = [target]
            pt = target

            while True:
                route.insert(0, resolus[pt][1]) # On ajoute au début de la liste de tuples-points le nouveau point
                pt = resolus[pt][1]
                if pt == start:
                    for i, e in enumerate(route): 
                        if i < len(route) - 1: a = '-'
                        else: a = ''
                        print(e.nom, end = a)
                    print(f'\nLongueur: {resolus[closest_point[0]][0]}')

                    for i, p in enumerate(route[:-1]):
                        shortest_path.append(make_name_from_vars([p, route[i+1]], '_'))
                        shortest_path.append(make_name_from_vars([route[i+1], p], '_'))
                    
                    return route
    
    # Dijkstra : On fait une liste de candidats et une liste de pts résolus. 
    # On a des tuples pour les points : (point, distance_depuis_départ, point_précédent)
    # À chaque itération, on prend le point P avec la plus petite distance depuis le départ,
    # puis on ajoute les tuples de ses voisins à candidats.
    # Le plus petit candidat devient résolu et c'est le nouveau point P pour l'itération n+1

def methode_aleatoire(start: Noeud, target: Noeud, iterations: int, trajets_complets = False):
    # La variable 'trajets_complets' permet de choisir parmis les options suivantes:
    # False (défaut) : Le programme calcule 'iterations' chemins différents sans prendre en compte combien atteignent l'arrivée (renvoie une erreur si aucun n'atteint l'arrivée);
    # True : Le programme calcule des chemins jusqu'à-ce que qu'il y en ait 'iterations' qui atteignent l'arrivée.

    global shortest_random_path

    start_time = time.time()

    calculated_paths = {}

    repetitions = iterations

    if trajets_complets: 
        completes = iterations # completes représente les trajets déja complétés atteignant l'arrivée
        iterations = 1

    loop = True
    while loop:

        current_point = start
        next_point = None

        visited_points = []
        
        while current_point != target:
            visited_points.append(current_point)
            # print(f'{visited_points=}')
            possible_points = [point for point in current_point.voisins if point not in visited_points]
            try :
                n = random.randint(0, len(possible_points) - 1)
            except:
                break
            next_point = possible_points[n]
            # print(next_point)
            current_point = next_point
        
        if current_point == target: 
            visited_points.append(current_point)
            calculated_paths[l:=longueur_chemin(visited_points)] = tuple(visited_points)
            # print("Point d'arrivée atteint. Longueur =", l)
            if trajets_complets:
                completes -= 1
        
        repetitions -= 1

        if trajets_complets: 
            iterations += 1
            if completes == 0:
                break
        elif repetitions == 0: break
            
    print(f"{iterations} trajets ont été testés. {len(calculated_paths)} atteignent le point d'arrivée.")
    # Si on demande que 1000 trajets atteignent l'arrivée mais que le programme affiche : "870 atteignent le point d'arrivée", 
    # c'est parce que 130 trajets ont déjà été trouvés. Donc 1000 trajets l'atteignent mais 130 sont présents plusieurs fois et pas comptabilisés.
    assert len(calculated_paths) != 0, "Aucun trajet n'atteint l'arrivée."
    min_length = min(list(calculated_paths.keys()))

    end_time = time.time()

    shortest_random_path = (min_path:=calculated_paths[min_length])

    print('Longueur min :', min_length)
    print('Chemin optimal :', min_path)
    print("Temps d'éxécution :", end_time - start_time)
    
    pass

#-----Fonction d'exécution du programme-----

def execute():
    global Points, Segments, nombre_points, trajet

    t1 = t2 = None
    iterations = 0

    t0 = time.time()
    
    while True:

        generePoints(nombre_points)
        iterations += 1

        t1 = time.time()
        trouvevoisins(Points)
        t2 = time.time()

        
        if cherche_iles(Points):
            break

        Points = []
        Segments = {}
    t3 = time.time()

    for i in Points:
        if Points[0] not in i.voisins: 
            Points[0].voisins.pop(Points[0].voisins.index(i))   # On enlève tous les points pas voisins avec P0 de P0.voisins
    Points[0].voisins.pop(Points[0].voisins.index(Points[0]))

    match iterations:
        case 1 : print(f'{iterations} graphe a été généré.')
        case n if n > 1: print(f'{iterations} graphes ont été générés.')

    t4 = time.time()
    print('\nDijkstra :')
    Dijkstra(Points[trajet[0]], Points[trajet[1]])
    t5 = time.time()
    
    print(f'------------------------------\nTemps de génération du graphe : {t3-t0}')
    print(f'Temps de recherche de voisins : {t2-t1}')
    print(f'Temps de calcul de l\'itinéraire optimal : {t5-t4}')
    print(f'Temps total : {t5-t0}')

    print('\nMéthode aléatoire :')
    methode_aleatoire(Points[trajet[0]], Points[trajet[1]], 100, True)

    export_graphe([Points, Segments])

    Affiche(Points, Segments)

#-----Affichage de Pygame sur l'ecran-----

def Affiche(points: list, segments: list):
    global shortest_path, shortest_random_path
    continuer = True
    couleurs = {
        'fond': BLANC,
        'segments': BLEU,
        'chemin optimal': ROUGE,
        'chemin optimal aléatoire': VERT,
        'points': BLEU,
        'noms': NOIR
    }

    points_chemin = []  # On va afficher les points du chemin court de la même couleur
    for i in shortest_path:
        points_chemin += i.split('_')

    while continuer:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False

        screen.fill(couleurs['fond'])

        segments_courts = []    # Les segments du chemin le plus court seront affichés par-dessus les autres
        for key, fig in segments.items():
            if key in shortest_path:    # Les segments du chemin le plus court seront affichés par-dessus les autres
                pygame.draw.line(screen, couleurs['chemin optimal'], segments[key].ext[0].pos, segments[key].ext[1].pos, 2)
            else:
                pygame.draw.line(screen, couleurs['segments'], fig.ext[0].pos, fig.ext[1].pos, 2) 

        segments_courts_methode_aleatoire = [pt for pt in points if pt in shortest_random_path]

        for fig in points:
            if fig.nom in points_chemin:
                pygame.draw.circle(screen, couleurs['chemin optimal'], fig.pos, fig.r)
                nomPoint = font.render(fig.nom, True, couleurs['chemin optimal'])
            elif fig in segments_courts_methode_aleatoire:
                pygame.draw.circle(screen, couleurs['chemin optimal aléatoire'], fig.pos, fig.r)
                nomPoint = font.render(fig.nom, True, couleurs['noms'])
            else :
                pygame.draw.circle(screen, couleurs['points'], fig.pos, fig.r)
                nomPoint = font.render(fig.nom, True, couleurs['noms'])
            screen.blit(nomPoint, [fig.pos[0]+fig.r, fig.pos[1]])

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

#-----Génération de points-----

def generePoints(nombre: int):
    global Points, taille
    for i in range(nombre):
        x = random.randint(10, taille[0]-30)
        y = random.randint(10, taille[1]-30)
        point = Noeud("P"+str(i), x, y, 3, [])

def trouvevoisins(Points: list):
    global Segments
    diagonale_plan = math.sqrt(taille[0]**2 + taille[1]**2)
    for i in Points:
        voisin1 = Edge(0, 0, diagonale_plan)
        voisin2 = Edge(0, 0, diagonale_plan)
        voisin3 = Edge(0, 0, diagonale_plan)
        for j in Points:
            if i != j:
                hypotenuse = pythagore(i,j)
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
        sortie = 0  # Sortir de la boucle si c'est inutile de continuer
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
        declaration = f'Noeud({point.nom}, {point.pos[0]}, {point.pos[1]}, {point.r}, {point.voisins})'
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

#-----Calcule la longueur d'un segment entre deux points-----
def longueur_segment(p1, p2):
    global Segments
    long = 0
    if make_name_from_vars([p1, p2], '_') in Segments:
        long = Segments[make_name_from_vars([p1, p2], '_')].long
    elif make_name_from_vars([p2, p1], '_') in Segments:
        long = Segments[make_name_from_vars([p2, p1], '_')].long
    return long

def longueur_chemin(route: list):
    long = 0
    dernier_point = None
    for point in route:
        if dernier_point != None:
            long += longueur_segment(dernier_point, point)
        dernier_point = point
    return long

#-----Calcule la distance entredeux points avec pythagore-----
def pythagore(p1, p2):
    return math.sqrt((p1.pos[0] - p2.pos[0])**2 + (p1.pos[1] - p2.pos[1])**2)


#===Constantes couleurs===

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (215, 215, 215)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
VERTFONCE = (48, 162, 38)
BLEUMARINE = (00, 25, 127)
ORANGE = (199, 95, 48)
CREME = (237, 225, 220)


#===Variables===

#-----Graphe-----

Points = []
Segments = {}
shortest_path = []
shortest_random_path = set()
nombre_points = 150
trajet = (0, nombre_points-1)   # L'index des points de départ et d'arrivée

#-----Affichage-----

taille = (1000, 700)


#===Exécution===

pygame.init()
pygame.display.set_caption(' Graphe')
screen = pygame.display.set_mode(taille)
clock = pygame.time.Clock()

#-----Texte-----

font = pygame.font.SysFont('Times New Roman', 16, True, False)

#-----Affichage-----

execute()