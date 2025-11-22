# projet_graphes_rabah_mohamed
code du projet 

membres du groupes 
Rabah TOUBAL & TIEMTORE Mohamed Haady






### Question 1 :

Etant donné la définition de voisinage dans ce problème (les cases en diagonales ne sont pas prises en compte), on peut modéliser une case par un sommet (soit blanc/soit noir). En construisant le graphe associé à l'échiqier mutilé (en reliant les sommets à leur voisins). Ainsi un sommet donné ne peut pas être voisin avec un autre sommet de même couleur. Aucune arête ne relie deux sommets du même côté. D'après la définition d'un graphe  biparti, on en déduit que la modélisation de ce problème revient donc à celle d'un graphe biparti. 

=> Donc le graphe représentant l'échiquer mutilé est bien un graphe biparti.





###### Version reformulée par GPT
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
