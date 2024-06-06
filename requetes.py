# Claire Deneau - Thomas Brossier
# Groupe : 2

# imports nécessaires ------------ #
import json
import networkx as nx
import matplotlib.pyplot as plt
# -------------------------------- #

# Graphes pour tester les fonctions suivantes # --------------------------------------------------------------------------------------------------------------- #
G_connexe = nx.Graph()
G_connexe.add_edges_from([("A", "B"), ("C", "B"), ("B", "D"), ("D", "E"), ("E", 'F'), ("F", "H"), ("H", "I"), ("H", "J"), ("E", "G"), ("E", "A"), ("E", "J")])
nx.draw(G_connexe)
# plt.show()

G_non_connexe = nx.Graph()
G_non_connexe.add_edges_from([("C", "B"), ("A", "B"), ("B", "D"), ("D", "E"), ("E", 'F'), ("E", "C"), ("G", "H")])
nx.draw(G_non_connexe)
# plt.show()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------ #

def nettoyageNoms(liste_noms):
    """Fonction clarifiant les noms d'une liste de noms en supprimant les caractères inutiles

    Args:
        liste_noms (list): liste des noms à nettoyer

    Returns:
        dict : liste des noms sans les caractères parasites
    """
    nettoyes = []
    for nom in liste_noms:
        sansCrochets = nom.replace('[', '').replace(']', '').replace("'", '')
        index = len(sansCrochets)
        if "(" in sansCrochets:
            index = min(index, sansCrochets.index("("))
        if "<" in sansCrochets:
            index = min(index, sansCrochets.index("<"))
        if "|" in sansCrochets:
            index = min(index, sansCrochets.index("|"))
        propre = sansCrochets[:index]
        nettoyes.append(propre.strip())
    return nettoyes
    
# Q1 - Échauffement
def json_vers_nx(filename):
    """Fonction convertissant le jeu de données en un graphe Networkx

    Args:
        filename (txt): _description_

    Returns:
        graph: Un graphe (networkx)
    """
    dico = {}
    # Nettoyage du fichier et lecture de celui-ci
    with open(filename, 'r') as file:
        for line in file.readlines():
            ligneConvertie = json.loads(line)
            if ligneConvertie["cast"]:
                dico[ligneConvertie["title"]] = nettoyageNoms(ligneConvertie["cast"])
    # Création du graphe avec Networkx            
    G = nx.Graph()
    for casting in dico.values():
        for u in casting:
            for v in casting:
                if u != v:
                    G.add_edge(u, v)
    return G

# Q2 - Collaborateurs communs
def collaborateurs_communs(G,u,v):
    """Fonction de recherche déterminant quels sont les acteurs qui ont collaboré avec les deux acteurs en paramètre.
    
    Parametres:
        G: le graphe
        u: acteur (sommet)
        v: acteur (sommet)
        
    Returns:
        set : liste des noms des acteurs ayant déjà travaillé avec les deux acteurs placés en paramètre
    """
    if u not in G.nodes:
        return u + " est inconnu"
    if v not in G.nodes:
        return v + " est inconnu"
    collaborateurs_en_commun = set()
    for collaborateur in G[u]:
        if collaborateur in G[v]:
            collaborateurs_en_commun.add(collaborateur)
    return collaborateurs_en_commun

# Q3 - Collaborateurs proches
def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G.
       La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs
        

def est_proche(G,u,v,k=1):
    """ Fonction déterminant si l'acteur v est proche de l'acteur u en utilisant la fonction collaborateurs_proches

    Args:
        G: le graphe
        u: le sommet de départ
        v: un autre sommet
        k: une distance

    Returns:
        bool : True si l'acteur v est proche de l'acteur u à distance k
    """
    collab_proche = collaborateurs_proches(G, u, k)
    return v in collab_proche

def distance_naive(G,u,v):
    """ Fonction déterminant la distance entre deux acteurs u et v

    Args:
        G: le graphe
        u: le sommet de départ
        v: un autre sommet

    Returns:
        int : la valeur de k si l'acteur est proche de l'autre. None sinon.
    """
    k = 1
    while k <= 5:
        if est_proche(G, u, v, k):
            return k
        k+=1
    return None

# Fonctions rajoutées
def est_connexe(G):
    """
    Fonction déterminant si un graphe est connexe ou non
    
    Args:
        G (graph) : un graphe dont on veut déterminer la connexité
        
    Returns:
        boolean : True si le graphe est connexe
    """
    def dfs(G, depart, visites):
        if depart not in visites:
            visites.add(depart)
        for suivant in set(G[depart]) - visites:
            dfs(G, suivant, visites)
        return visites
    return len(G) == len(dfs(G, list(G.nodes)[0], set()))
# FIN

def distance(G,u,v):
    """Fonction déterminant la nombre d'arêtes séparant deux acteurs dans un graphe donné

    Args:
        G (graph): graphe
        u (str): nom de l'acteur de départ
        v (str): nom de l'acteur d'arrivée

    Returns:
        int: distance entre les deux acteurs
    """
    if u == v :
        return 0
    if not(u in G.nodes and v in G.nodes):
        return "L'un des deux acteurs ne fait pas partie du graphe."
    if not est_connexe(G):
        return "Le graphe n'est pas connexe, distance incalculable."
    collaborateurs = {u}
    distance = 0
    while v not in collaborateurs:
        collaborateurs_directs = set()
        for acteur in collaborateurs:
            for voisin in G[acteur]: 
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
            collaborateurs = collaborateurs.union(collaborateurs_directs)
        distance +=1
    return distance
    
# Q4 - Qui est au centre d'Hollywood ?

# Q5 - Une petite famille
def eloignement_max(G):
    """Fonction déterminant la distance séparant les deux noeuds les plus éloignés d'un graphe donné

    Args:
        G (nx.Graph): le graphe
        
    Returns:
        int: distance maximum entre deux noeuds
    """
    if not est_connexe(G):
        return "Le graphe n'est pas connexe, distance maximum incalculable"
    distances = []
    for acteur in G.nodes:
        collaborateurs = {acteur}
        i = 0
        while i < len(G.nodes) and len(collaborateurs) < len(G.nodes):
            collaborateurs_directs = set()
            for c in collaborateurs:
                for voisin in G.adj[c]:
                    if voisin not in collaborateurs:
                        collaborateurs_directs.add(voisin)
            collaborateurs = collaborateurs.union(collaborateurs_directs)
            i+=1
        distances.append(i)
    return max(distances)

# Tests avec les graphes connexe et non connexe créé au début :
#Q2 - Assert
assert collaborateurs_communs(G_connexe, 'E', 'H') == {'J', 'F'}
assert collaborateurs_communs(G_non_connexe, 'E', 'H') == set()
#Q3 - Assert
assert collaborateurs_proches(G_connexe, 'B', 2) == {'A', 'B', 'C', 'D', 'E'}
assert collaborateurs_proches(G_non_connexe, 'H', 3) == {'G', 'H'}
assert est_connexe(G_connexe)
assert not (est_connexe(G_non_connexe))
assert distance(G_connexe, 'A', 'H') == 3
assert distance(G_non_connexe, 'A', 'H') == "Le graphe n'est pas connexe, distance incalculable."
assert distance_naive(G_connexe,'A','H') == 3
assert distance_naive(G_non_connexe,'A','H') == None
#Q4 - Assert
assert centralite(G_connexe, 'E') == 3
assert centralite(G_connexe, 'H') == 5
assert centralite(G_non_connexe, 'H') == "Le graphe n'est pas connexe, centralité incalculable."

assert centre_hollywood(G_connexe) == "E"
assert centre_hollywood(G_non_connexe) == "Le graphe n'est pas connexe, centralité incalculable."
#Q5 - Assert
assert eloignement_max(G_connexe) == 6
assert eloignement_max(G_non_connexe) == "Le graphe n'est pas connexe, distance maximum incalculable."
    
# Tests avec Hollywood

print("\n Tests avec Hollywood - 100")

# Q1 - Échauffement
print("\n Affichage graphe ...")
Hollywood = json_vers_nx('data_100.txt')
nx.draw(Hollywood)
plt.show()

# Q2 - Collaborateurs communs

# Q3 - Collaborateurs proches
print("\n Q3 - Collaborateurs proches")
print(f"Collaborateurs proches de Frank Oz avec k = 2 : {collaborateurs_proches(Hollywood, 'Frank Oz', 2)}")
print(f"Test distance naïve : {distance_naive(G_connexe,'A','H')}")
print(f"Test distance naïve : {distance_naive(G_non_connexe,'A','H')}")
print("Collaborateurs proches - Connexité")
print(f"Le graphe Hollywood est connexe ? : {est_connexe(Hollywood)}")
print("Collaborateurs proches - distance")
print(f"Distance entre Tony Roberts et Bernard Barrow : {distance(Hollywood, 'Tony Roberts', 'Bernard Barrow')}")

# Q4 - Qui est au centre d'Hollywood ?
def centralite(G,u):
    """Fonction déterminant la distance entre un acteur et l'acteur le plus éloigné de lui d'un graphe donné
    
    Args:
        G (graph): graphe des acteurs
        u (str): nom de l'acteur dont on veut déterminer la centralité
        
    Returns:
        int : centralité de l'acteur
    """
    if not est_connexe(G):
        return "Le graphe n'est pas connexe, centralité incalculable."
    return distance(G, u, max(G.nodes, key=lambda node : distance(G, u, node)))
    
def centre_hollywood(G):
    """Fonction déterminant l'acteur le plus central d'un graphe
    
    Args:
        G (graph): graphe d'acteurs
    
    Returns:
        str : nom de l'acteur le plus central
    """
    if not est_connexe(G):
        return "Le graphe n'est pas connexe, centralité incalculable."
    centralites = {acteur : centralite(G, acteur) for acteur in G.nodes}
    return min(centralites, key=lambda acteur : centralites[acteur])
# Q5 - Une petite famille
print("\n Q5 - Une petite Famille - eloignement_max")
print(f"Eloignement maximum sur le graphe d'Hollywood : {eloignement_max(Hollywood)}")
