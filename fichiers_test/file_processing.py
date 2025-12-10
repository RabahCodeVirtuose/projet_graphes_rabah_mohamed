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
    Transforme le board en graphe biparti G compatible avec tes fonctions.
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
