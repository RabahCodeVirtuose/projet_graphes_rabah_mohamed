def read_board(filename):
    """
    Lit un fichier échiquier mutilé.
    Retourne un tableau 2D board[i][j] ∈ {"B", "N", "X"}.
    """
    with open(filename, "r") as f:
        n = int(f.readline().strip())
        board = []
        for _ in range(n):
            row = f.readline().strip().split()
            board.append(row)
    return board


def construire_graphe_depuis_board(board):
    """
    Transforme le board en graphe G.
    Chaque sommet est une chaîne : 'B_i_j' ou 'N_i_j'.
    """
    n = len(board)
    G = {}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    for i in range(n):
        for j in range(n):
            case = board[i][j]
            if case == "X":
                continue

            u = f"{case}_{i}_{j}"
            G[u] = []

            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and board[ni][nj] != "X":
                    v_case = board[ni][nj]
                    v = f"{v_case}_{ni}_{nj}"
                    G[u].append(v)

    return G



def extract_indices(node_name):
    """ Extrait les indices (ligne i, colonne j) d'un nom de sommet encodé 'C_i_j'. """
    # Ex: 'B_7_7' -> (7, 7)
    _, i, j = node_name.split('_')
    return int(i), int(j)


def export_dominos_matrix(M, board, filename):
    
    N = len(board) # Taille de la matrice (N x N)
    
    # 1. Créer la nouvelle matrice de pavage (initialisée à 'X' ou '0')
    # copie de la matrice d'entrrée avec des modifs 
    paving_matrix = [['X'] * N for _ in range(N)]
    
    # On initialise les cases non interdites à 0 
    for r in range(N):
        for c in range(N):
            if board[r][c] != 'X':
                paving_matrix[r][c] = 0 # 0 = case non pavée
                
    # 2. Remplir la matrice avec les dominos (numérotés de 1 à t)
    domino_number = 1
    for u, v in M:
        # Récupère les indices pour u et v
        r_u, c_u = extract_indices(u)
        r_v, c_v = extract_indices(v)
        
        # Affecter le numéro du domino aux deux positions
        paving_matrix[r_u][c_u] = domino_number
        paving_matrix[r_v][c_v] = domino_number
        
        domino_number += 1
        
    with open(filename, "w") as f:
        for row in paving_matrix:
            # Convertir les entiers en chaînes (avec espace de séparation)
            # Les 'X' restent 'X'
            row_str = " ".join(map(str, row))
            f.write(row_str + "\n")
