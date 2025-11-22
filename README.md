# projet_graphes_rabah_mohamed
code du projet 

membres du groupes 
Rabah TOUBAL & TIEMTORE Mohamed Haady






### Question 1 :

Etant donné la définition de voisinage dans ce problème (les cases en diagonales ne sont pas prises en compte), on peut modéliser une case par un sommet (soit blanc/soit noir). En construisant le graphe associé à l'échiqier mutilé (en reliant les sommets à leur voisins). Ainsi un sommet donné ne peut pas être voisin avec un autre sommet de même couleur. Aucune arête ne relie deux sommets du même côté. D'après la définition d'un graphe  biparti, on en déduit que la modélisation de ce problème revient donc à celle d'un graphe biparti. 

=> Donc le graphe représentant l'échiquer mutilé est bien un graphe biparti.





###### Version reformulée 
Étant donné la définition du voisinage dans ce problème (les cases en diagonale ne sont pas prises en compte), on modélise chaque case par un sommet, coloré en blanc ou noir comme dans un damier. En construisant le graphe associé à l’échiquier mutilé, on relie deux sommets si leurs cases sont adjacentes orthogonalement. Or deux cases adjacentes ont toujours des couleurs opposées : un sommet blanc ne peut donc être adjacent qu’à un sommet noir, et réciproquement. Ainsi, aucune arête ne relie deux sommets d’une même couleur. D’après la définition d’un graphe biparti, ce graphe est bien biparti.


### Question 2 : 

Dans l'échiquier (sous la forme d'un graphe G = (V,E)), on peut remarquer que 
1. Chaque case a au plus 4 voisins donc : 
    - deg(v) <= 4 
  
2. La somme des dégrés de ce graphe (échiquier mutilé) :
 - Somme des deg(v) <= 4n (avec n le nombre de sommets)

3. On sait que Somme des deg(v) (pour tout v element de V) = 2|E|.

=> On en conclut que 2|E| <= 4n   => |E| <= 2n. 



### Question 3 : 


couplage parfait, => Tous les sommets sont couverts.  
couplage simple => On peut avoir des sommets non couverts.

On peut voir un domino comme une arête entre 2 sommets noir et blanc. L'objectif etant de paver l'échiquier tout entier (échiquier étant un graphe biparti comme démontré precedemment), celà revient à chercher à couvrir 2 cases voinses (2 sommets) avec un domino.

Parvenir donc à couvrir otous les sommets avec les dominos, revient à chercher un couplage parfait pour ce graphe.



###### Version reformulée : 

Couplage parfait => tous les sommets sont couverts.
Couplage simple => certains sommets peuvent rester non couverts.

On peut voir un domino comme une arête reliant deux sommets, un noir et un blanc. L’objectif étant de paver toutes les cases de l’échiquier (modélisé comme un graphe biparti, comme démontré précédemment), cela revient à couvrir deux cases voisines (deux sommets) avec un domino.

Parvenir à couvrir tous les sommets avec les dominos revient donc à chercher un couplage parfait pour ce graphe.








### Question 3 (Rabah) : 

Dans le graphe modélisant l’échiquier mutilé, chaque sommet représente une case, et chaque arête relie deux cases adjacentes. Une arête correspond donc à un emplacement possible pour un domino.

Un couplage est un ensemble d’arêtes qui ne partagent aucun sommet : cela représente un ensemble de dominos placés sans chevauchement.
Un couplage parfait est un couplage dans lequel chaque sommet appartient exactement à une arête. Cela signifie que chaque case est couverte par un unique domino.

Ainsi, un couplage parfait correspond exactement à un pavage complet de l’échiquier par des dominos.
Si un couplage parfait existe, alors le pavage est possible ; sinon, il est impossible de recouvrir toutes les cases restantes avec des dominos.
