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
    #print(N) # debug 
    #print(B) # debug 
    
    '''for u in G :
        for v in G[u] :
            if u in N and v in B :
                if M.get(u) == v : 
                    if u not in GM[v] : # Suppression des doublons 
                        GM[v].append(u) 
                else : 
                    if v not in GM[u] : # Suppression des doublons 
                        GM[u].append(v) 
            elif u in B and v in N : 
                if M[u] == v  :
                    if v not in GM[u] : # Suppression des doublons 
                        GM[u].append(v)
                else : 
                    if u not in GM[v] : # Suppression des doublons 
                        GM[v].append(u)
                
    return GM '''
    ## M est  maintenant un set => Adaptation 
    for u in G:
        for v in G[u]:
            if u in N and v in B:
                if (u,v) in M:
                    if u not in GM[v]:
                        GM[v].append(u)
                else:
                    if v not in GM[u]:
                        GM[u].append(v)
            elif u in B and v in N:
                if (u,v) in M or (v,u) in M:
                    if v not in GM[u]:
                        GM[u].append(v)
                else:
                    if u not in GM[v]:
                        GM[v].append(u)
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
    return libres_N, libres_B'''
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
    
  
    
    
def dfs_augmentant(u, niveau, HT, chemin, chemins):
    if niveau[u] == 0:
        chemins.append(list(reversed(chemin + [u])))
        return

    for v in HT[u]:
        if niveau[v] == niveau[u] - 1:
            dfs_augmentant(v, niveau, HT, chemin + [u], chemins)
    
    

def chemins_augmentants(HT, niveau, B, libres_B):
    # pour chaque sommet libre dans B au niveau k,
    # on remonte dans HT jusqu'à atteindre un sommet au niveau 0
    chemins = []

    for b in libres_B:
        if b not in niveau:
            continue

        dfs_augmentant(b, niveau, HT, [], chemins)

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
        P = chemins_augmentants(H_reversed, niveau, B, libres_B)

        # 6. Si aucun chemin → fini
        if not P:
            break

        # 7. Appliquer les augmentations
        for p in P:
            M = M.symmetric_difference(p)    # symmetric difference

    return M

        
        
        

        
        

        
        
    
    
    
    

##### Si tu lis ça, Rabah, faudrait qu'on se voit pour que je t'explique plus en profondeur ce que j'ai compris !