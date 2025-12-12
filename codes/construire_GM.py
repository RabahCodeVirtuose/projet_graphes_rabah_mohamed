from collections import deque

def bipartition(G):
    """
    Détermine et retourne les deux partitions (N et B) d'un graphe biparti G.
    Utilise un parcours en largeur (BFS) pour colorier les sommets.

    Args:
        G (dict): Le graphe d'entrée, représenté par un dictionnaire d'adjacence.

    Returns:
        tuple: Un tuple contenant deux ensembles (sets) de sommets:
               - N (set): L'ensemble des sommets de la partition 0.
               - B (set): L'ensemble des sommets de la partition 1.
               
    Note: Si le graphe n'est pas connexe, la bipartition s'applique à toutes les composantes.
    """
    color = {}
    
    for start in G:
        if start not in color:
            color[start] = 0
            queue = deque([start])
            
            while queue:
                u = queue.popleft()
                for v in G[u]: # Pour chaque voisin de v 
                    if v not in color: # si v n'est pas coloré
                        color[v] = 1 - color[u] # on lui donne la couleur opposée 
                        queue.append(v) # on ajoute v à la file pour continuer la progression 
    
    N = {u for u in color if color[u] == 0}
    B = {u for u in color if color[u] == 1}
    return N, B



def construire_GM(G, M) :
    """
    Construit le graphe résiduel G_M orienté à partir du graphe biparti G 
    et du couplage actuel M.

    Args:
        G (dict): Le graphe biparti d'origine (non orienté).
        M (set): Le couplage actuel, un ensemble d'arêtes orientées (u, v) où u ∈ N et v ∈ B.

    Returns:
        dict: Le graphe résiduel GM, représenté par un dictionnaire d'adjacence orienté.
    """
    GM = {u: [] for u in G}
        
    N, B = bipartition(G)
    # On garantit que toutes les arêtes (u,v) de G sont traitées une fois
    for u in N: # On ne parcourt que N
        for v in G[u]: # Voisin de u, doit être dans B
            if (u, v) in M: # Arête couplée
                # Arête B -> N (v -> u)
                GM[v].append(u)
            else: # Arête non couplée
                # Arête N -> B (u -> v)
                GM[u].append(v)
    return GM
    

def sommets_libres(M, N, B): # M est le couplage , qu'on a 
    """
    Détermine les sommets non couverts par le couplage M dans chacune des partitions N et B.

    Args:
        M (set): Le couplage actuel, ensemble d'arêtes (n, b).
        N (set): La partition gauche du graphe.
        B (set): La partition droite du graphe.

    Returns:
        tuple: Un tuple contenant deux ensembles (sets):
               - libres_N (set): Les sommets libres dans la partition N.
               - libres_B (set): Les sommets libres dans la partition B.
    """
    libres_N = {u for u in N if all(u not in edge for edge in M)}
    libres_B = {v for v in B if all(v not in edge for edge in M)}
    return libres_N, libres_B




def construire_niveaux(GM, libres_N, libres_B):
    """
    Construit le sous-graphe à niveaux H du graphe résiduel GM.
    Utilise un parcours en largeur pour assigner un niveau à chaque sommet 
    à partir des sommets libres de N (niveau 0).
    Détermine la longueur k du plus court chemin augmentant (vers un sommet libre de B).

    Args:
        GM (dict): Le graphe résiduel G_M orienté.
        libres_N (set): Les sommets libres dans la partition N (utilisés comme source).
        libres_B (set): Les sommets libres dans la partition B (utilisés comme destination).

    Returns:
        tuple: Un tuple contenant:
               - H (dict): Le sous-graphe à niveaux, contenant uniquement les arcs allant de niveau i à i+1, et s'arrêtant au niveau k.
               - niveau (dict): Le dictionnaire des niveaux {sommet: niveau}.
    """
    niveau = {}
    queue = deque()

    # niveau 0 = libres_N
    for u in libres_N:
        niveau[u] = 0
        queue.append(u)

    k = float('inf')

    while queue:
        u = queue.popleft()
        for v in GM[u]:
            if v not in niveau:
                niveau[v] = niveau[u] + 1
                queue.append(v)
                if v in libres_B:
                    k = niveau[v]

    # On ne garde que les sommets jusqu'au niveau k
    H = {u: [] for u, lvl in niveau.items() if lvl <= k}

    # On conserve uniquement les arcs menant à un niveau suivant
    for u in H:
        H[u] = [v for v in GM[u]
                if v in H and niveau[v] == niveau[u] + 1]

    return H, niveau
                


def renverser(H) :
    """
    Calcule l'inverse H_T du graphe H, en inversant le sens de tous les arcs.
    Utilisé pour remonter les chemins augmentants du niveau k (libres_B) au niveau 0 (libres_N) 
    avec un parcours en profondeur.

    Args:
        H (dict): Le sous-graphe à niveaux, orienté (niveau i -> niveau i+1).

    Returns:
        dict: Le graphe inversé H_T, orienté (niveau i+1 -> niveau i).
    """
    
    sommets = set(H.keys())
    for u in H:
        for v in H[u]:
            sommets.add(v)

    H_T = {u: [] for u in sommets}
    
    # inverse les arêtes
    for u in H:
        for v in H[u]:
            H_T[v].append(u)

    return H_T
    
  
    
    
def dfs_augmentant(u, niveau, HT, chemin, chemins, N,bloques):
    """
    Parcours en profondeur (DFS) pour trouver un chemin augmentant à partir du sommet u 
    dans le graphe transposé H_T, remontant du niveau k vers le niveau 0.

    Args:
        u : Le sommet courant à visiter.
        niveau (dict): Le dictionnaire des niveaux {sommet: niveau}.
        HT (dict): Le graphe transposé H_T (niveau i+1 -> niveau i).
        chemin (list): La liste des sommets visités jusqu'à u (chemin partiel).
        chemins (list): La liste où les sets d'arêtes des chemins augmentants complets sont stockés.
        N (set): L'ensemble des sommets de la partition N (pour l'orientation N->B).
        bloques (set): L'ensemble des sommets déjà utilisés dans un chemin augmentant trouvé 
                       dans cette phase BFS (pour garantir le caractère disjoint des chemins).

    Returns:
        bool: True si un chemin augmentant a été trouvé depuis u, False sinon.
    """
    
    
    if niveau[u] == 0:
        arcs = set()
        full_path = list(reversed(chemin + [u]))
        
        # Le sommet de niveau 0 (dans N) est maintenant inclus dans le path
        
        for i in range(len(full_path)-1):
            a, b = full_path[i], full_path[i+1]
            
            # ORIENTATION : Toujours N -> B
            if a in N:
                arcs.add((a, b))
            else:
                arcs.add((b, a))
        
        chemins.append(arcs)
        
        # Blocage de tous les sommets du chemin
        for node in full_path:
            bloques.add(node)
        
        return True # Chemin trouvé
    
    # DFS récursif
    for v in HT[u]:
        # On vérifie si v est bloqué avant de descendre
        if niveau[v] == niveau[u] - 1 and v not in bloques:
            
            # Si l'appel récursif trouve un chemin...
            if dfs_augmentant(v, niveau, HT, chemin + [u], chemins, N, bloques):
                # ...le chemin entier est bloqué. On arrête de chercher d'autres chemins partant de u.
                # Ceci garantit qu'un sommet (u) ne participe qu'à un seul chemin dans cette phase.
                # Marquer u comme bloqué est déjà fait par le blocage du full_path.
                return True
    
    return False # Pas de chemin trouvé partant d'ici



def chemins_augmentants(HT, niveau, libres_B, N):
    """
    Génère l'ensemble maximal de chemins augmentants les plus courts (M-disjoints) 
    dans le sous-graphe H.

    Args:
        HT (dict): Le graphe transposé H_T.
        niveau (dict): Le dictionnaire des niveaux.
        libres_B (set): Les sommets libres dans la partition B (points de départ du DFS).
        N (set): L'ensemble des sommets de la partition N.

    Returns:
        list: Une liste de sets, où chaque set représente les arêtes orientées (N->B) 
              d'un chemin augmentant.
    """
    
    chemins = []
    bloques = set()

    for b in libres_B:
        if b not in niveau or b in bloques: # Ne pas partir d'un libre_B déjà utilisé
            continue
            
        dfs_augmentant(b, niveau, HT, [], chemins, N, bloques)

    return chemins


def Hopcroft_Karp(G):
    """
    Implémente l'algorithme de Hopcroft-Karp pour trouver un couplage de cardinalité maximale 
    dans un graphe biparti.

    L'algorithme procède par phases itératives, où chaque phase (BFS puis DFS) trouve 
    un ensemble maximal de chemins augmentants les plus courts de longueur k.

    Args:
        G (dict): Le graphe biparti d'entrée, représenté par un dictionnaire d'adjacence non orienté.

    Returns:
        set: Le couplage final M, représenté par un ensemble d'arêtes orientées (u, v) où u ∈ N et v ∈ B.
    """
    N, B = bipartition(G)
    M = set()            # couplage initial
       
    while True:
        
        # 1. Construire GM
        GM = construire_GM(G, M)

        # 2. Sommets libres
        libres_N, libres_B = sommets_libres(M, N, B)

        # 3. Construire niveaux
        H, niveau = construire_niveaux(GM, libres_N, libres_B)

        # 4. Renverser
        H_reversed = renverser(H)

        # 5. Chemins augmentants
        P = chemins_augmentants(H_reversed, niveau, libres_B, N)

        # 6. Si aucun chemin -> fini
        if not P:
            break

        # 7. Appliquer les augmentations
        for arcs_du_chemin in P:
            M = M.symmetric_difference(arcs_du_chemin)

    return M

        
        
        

        
        

        
        
    
    
    
    

