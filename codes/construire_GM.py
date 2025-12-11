from collections import deque




# Graphe (mini exemple)

'''G = {
    "n1": ["b1", "b2"],
    "n2": ["b1"],
    "n3": [],
    "b1": ["n1", "n2"],
    "b2": ["n1"]
}


## Juste un exemple de couplage vide au début
M = {
    "n1" : None,
    "n2" : None, 
    "n3" : None, 
    "b1" : None, 
    "b2" : None
}

'''

def bipartition(G):
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
    GM = {u: [] for u in G}
        
    N, B = bipartition(G)
    # On garantit que toutes les arêtes (u,v) de G sont traitées une fois
    for u in N: # On ne parcourt que N
        for v in G[u]: # Voisin de u, doit être dans B
            if (u, v) in M: # Arête couplée
                # Arête résiduelle B -> N (v -> u)
                GM[v].append(u)
            else: # Arête non couplée
                # Arête résiduelle N -> B (u -> v)
                GM[u].append(v)
                
    # Pour les arêtes couplées dans M, on s'assure que B->N est dans GM
    # (ce qui est déjà fait ci-dessus si G[u] pour u in N couvre toutes les arêtes)
    
    return GM
    
  
############################################################################################ construire_niveaux 

def sommets_libres(M, N, B): # M est le couplage , qu'on a 
    """
    Renvoie deux ensembles : 
    - les sommets libres de N
    - les sommets libres de B
    """
    '''libres_N = {u for u in N if M[u] is None}
    libres_B = {v for v in B if M[v] is None}
    return libres_N, libres_B
    Un sommet u est libre s'il n'apparaît dans aucune arête du couplage M

    '''
    libres_N = {u for u in N if all(u not in edge for edge in M)}
    libres_B = {v for v in B if all(v not in edge for edge in M)}
    return libres_N, libres_B




def construire_niveaux(GM, libres_N, libres_B):
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
                
   


######################################################################################### renverser



def renverser(H) :
    
    
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
    DFS qui remonte du sommet u jusqu'au niveau 0.
    - chemin : liste des sommets visités
    - chemins : liste des chemins sous forme de sets d'arêtes orientées N->B
    - N : ensemble des sommets de la partition N pour orientation
    """
    # La vérification de u in bloques sera faite par l'appelant pour le sommet de départ
    
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
        
        return True # Chemin trouvé!
    
    
    

    # DFS récursif
    for v in HT[u]:
        # On vérifie si v est bloqué AVANT de descendre.
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
    Parcours tous les sommets libres de B et récupère les chemins augmentants
    sous forme de sets d'arêtes (u ∈ N, v ∈ B)
    """
    chemins = []
    bloques = set()

    for b in libres_B:
        if b not in niveau or b in bloques: # Ne pas partir d'un libre_B déjà utilisé
            continue
            
        dfs_augmentant(b, niveau, HT, [], chemins, N, bloques)

    return chemins




'''
Résumé des fonctions principales en présence : 
=> Construire_GM(G)
=> Construire_niveaux(GM)
=> Renverser(H)
=> chemins_augmentants(HT, niveau, B, libres_B).


Fonctions utilitaires : 

->bipartition(G) (nous retourne la bi-partition)
-> sommets_libres(M,N,B) (nous retourne les chemins libres des partitions N et B,
    avec M le couplage).
-> dfs_augmentant(u, niveau, HT, chemin, chemins) (DFS à partir d'un sommet libre
    u de niveau k dans la partition de droite B par arriver à un sommet de 
    dégré 0 dans la partition de gauche N).

'''


def Hopcroft_Karp(G):

    N, B = bipartition(G)
    M = set()            # couplage
       
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

        # 6. Si aucun chemin → fini
        if not P:
            break

        # 7. Appliquer les augmentations
        for arcs_du_chemin in P:
            # on transforme chaque chemin de sommets en set d’arêtes
            M = M.symmetric_difference(arcs_du_chemin)

    return M

        
        
        

        
        

        
        
    
    
    
    

##### Si tu lis ça, Rabah, faudrait qu'on se voit pour que je t'explique plus en profondeur ce que j'ai compris !