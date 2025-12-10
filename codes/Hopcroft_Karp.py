#from fichiers_test import file_processing  

import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from codes.construire_GM import Hopcroft_Karp


from fichiers_test.file_processing import read_board, construire_graphe_depuis_board


def export_dominos(M, filename):
    """
    Exporte le pavage en fichier : chaque arête du matching M = un domino.
    Chaque arête est un tuple (u,v).
    On numérote les dominos de 1 à t.
    """
    exported = set()  # pour éviter de doubler les arêtes (u,v) et (v,u)
    with open(filename, "w") as f:
        for i, (u,v) in enumerate(M, 1):
            # ignorer les arêtes déjà exportées dans l'autre sens
            if (v,u) in exported:
                continue
            f.write(f"{i} : {u} - {v}\n")
            exported.add((u,v))



# 1. Lire le fichier
board = read_board("../fichiers_test/echiquier_format.txt")

# 2. Construire le graphe biparti
G = construire_graphe_depuis_board(board)

# 3. Passer à Hopcroft-Karp
M = Hopcroft_Karp(G)

# 4. Vérifier pavage possible
nb_cases = sum(cell != "X" for row in board for cell in row)
pavage_possible = len(M) == nb_cases // 2
print(pavage_possible)
if pavage_possible :
    print("Nombres de dominos possibles : ", nb_cases // 2)
    export_dominos(M, "../results/dominos.txt")       
