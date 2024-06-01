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

# Q1 - Échauffement

# Q2 - Collaborateurs communs

# Q3 - Collaborateurs proches

# Fonctions rajoutées

# FIN

# Q4 - Qui est au centre d'Hollywood ?

# Q5 - Une petite famille

# Tests avec Hollywood