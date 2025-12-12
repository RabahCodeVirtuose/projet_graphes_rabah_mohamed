import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from codes.construire_GM import Hopcroft_Karp
from fichiers_test.file_processing import read_board, construire_graphe_depuis_board, export_dominos_matrix



def main(filepath):
    # Lire l'échiquier
    board = read_board(filepath)

    # Construire le graphe biparti
    G = construire_graphe_depuis_board(board)

    # Trouver un matching maximal
    M = Hopcroft_Karp(G)

    nb_cases = sum(cell != "X" for row in board for cell in row)
    #pavage_possible = len(M) == nb_cases // 2
    
    if nb_cases % 2 != 0:
        # Impair -> impossible de paver parfaitement
        pavage_possible = False
    else:
        # Pair -> possible seulement si |M| atteint |V|/2
        pavage_possible = len(M) == nb_cases // 2
        
        
    print(f"Pavable ? : {pavage_possible}")
        
    if pavage_possible:
        print(f"Nombre de dominos possibles : {nb_cases // 2}")
        base_name = os.path.basename(filepath) # Ex: 'smallboard.txt'
        output_filename = f"results/dominos_{base_name}" # Ex: 'results/dominos_smallboard.txt'
        export_dominos_matrix(M, board, output_filename)
    
        print("\n--- Infos du Graphe ---")
        print("Board lu =")
        for row in board:
            print(row)
        print(f"Nombre de cases non X = {nb_cases}")
        #print(f"Taille du matching = {len(M)}")
        print(f"Nombre de dominos possibles = {nb_cases // 2}")
        print("----------------------\n")
    else :   
        print("\n--- Infos du Graphe ---")
        print("Board lu =")
        for row in board:
            print(row)
        print(f"Nombre de cases non X = {nb_cases}")
        print(f"Nombre de dominos max = {nb_cases // 2}")
        print("----------------------\n")
        
    return pavage_possible