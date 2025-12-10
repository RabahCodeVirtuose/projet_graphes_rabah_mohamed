from collections import deque




# Graphe (mini exemple)
G = {
    "n1": ["b1", "b2"],
    "n2": ["b1"],
    "n3": [],
    "b1": ["n1", "n2"],
    "b2": ["n1"]
}


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


## Juste un exemple de couplage vide au début
M = {
    "n1" : None,
    "n2" : None, 
    "n3" : None, 
    "b1" : None, 
    "b2" : None
}




def construire_GM(G, M) :
    GM = {u: [] for u in G}
    N, B = bipartition(G)
    
    
    
    print(N) # debug 
    print(B) # debug 
    
    for u in G :
        for v in G[u] :
            if u in N and v in B :
                if M[u] == v : 
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
                
    return GM 
    
    
GM = construire_GM(G, M)

############################################################################################ construire_niveaux 

def sommets_libres(M, N, B): # M est le couplage , qu'on a 
    """
    Renvoie deux ensembles : 
    - les sommets libres de N
    - les sommets libres de B
    """
    libres_N = {u for u in N if M[u] is None}
    libres_B = {v for v in B if M[v] is None}
    return libres_N, libres_B




def construire_niveaux(GM) :
    libres_N, libres_B = sommets_libres(M, N, B) # M est notre couplage 

# Initialisation du BFS
    niveau = {}
    queue = deque()

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
                k = min(k, niveau[v])
                
                
    H_sommets = {u for u, lvl in niveau.items() if lvl <= k} ## Les sommets situés à une distance supérieure à k dans GM n’appartiennent pas à H => voir sujet
    
    H = {}
    for u in H_sommets:
        # on ne garde que les arcs vers le niveau suivant
        H[u] = [v for v in GM[u] if v in H_sommets and niveau[v] == niveau[u] + 1]

    return H, niveau # on va aussi recup le dict de niveau 
                
                
N, B = bipartition(GM)  # récupère la bipartition du graphe

#H, niveau = construire_niveaux(M,N,B)  


######################################################################################### renverser



def renverser(H) :
    
    
    sommets = set(H.keys())
    for u in H:
        for v in H[u]:
            sommets.add(v)

    H_T = {u: [] for u in sommets}
    
    # inverser les arêtes
    for u in H:
        for v in H[u]:
            H_T[v].append(u)

    return H_T
    
    

H , niveau= construire_niveaux(M,N,B)
H_prime = renverser(H) 



'''def chemins_augmentants(M, N, B) :
    libres_N, libres_B = sommets_libres(M, N, B)
    P = []
    for i in libres_B : ## Que des sommets libres de B de niveau k 
        path_list = list(DFS(i))
        B.remove(i) 
        
    P.append(path_list)
    return P 
    libres_k = {b for b in libres_B if niveau[b] == k}

    for b in libres_k:
        chemin = dfs_vers_niveau_0(H_T, b, niveau, libres_N)
        if chemin is not None:
            P.append(chemin)

    return P'''
    
    
    
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


 
N, B = bipartition(G)
libres_N, libres_B = sommets_libres(M, N, B)
H , niveau= construire_niveaux(M,N,B)
HT = renverser(H)
P = chemins_augmentants(HT, niveau, B, libres_B)



##### Si tu lis ça, Rabah, faudrait qu'on se voit pour que je t'explique plus en profondeur ce que j'ai compris !