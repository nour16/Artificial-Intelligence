# Rapport de projet

## Groupe
* BESSAD Melina
* KLICH NourElHouda

## Description des choix importants d'implémentation
* Nous avons organisé notre projet en 03 fichiers :
    * **strategie.py** : qui contient le code de toutes les stratégies :
        * *aleatoire* : 
            * Prend en arguments :
                - players : une liste de joueurs
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
            * Cette stratégie attribue à chaque militant un électeur aléatoirement, elle renvoie une liste des buts(positions d'électeurs) attribués aux militants.
        * *tetu* :
            * Prend en arguments :
                - players : une liste des joueurs
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
            * Cette stratégie attribue à chaque militant un électeur fixe. Un militant m aura donc pour electeur d'indice *** m % len(goalStates) ***
            et il gardera celui-ci jusqu'à la fin de la compagne
        * *StochastiqueExper* :
            * Prend en arguments : 
                - joueurs : une liste de tuples représentant les positions des joueurs de l'équipe 
                - ennemis : une liste de tuples représentant les positions des joueurs de l'équipe adverse   
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
                - jour : un entier représentant le numéro de la journée 
                - strategies : une liste qui contient le noms de toutes les stratégies que l'on a implémentées sauf la StochastiqueExpert
            * Cette stratégie génére une liste de probabilités comprises entre 0 et 1 (probaStrat). Cette liste est de meme taille que la liste des stratégies passées en paremètres, elle fait correspondre chaque stratégie à une probabilité de la liste.
            Ensuite, elle tire un nombre au hasard p (entre 0 et 1), elle calcule les différences entre p et les probabilités dans la liste des probabilités probaStrat et stcoke ces différences dans une liste. Elle renvoie la stratégie dont l'indice correspond à la l'indice de la plus petite différence. Elle applique cette stratégie sur les joueurs avec la fonction jouer_stratégie (qu'on eexpliquera plus tard), elle renvoie la liste des buts généré par la stratégie choisie.
        * *meilleureReponse* :
            * Prend en arguments :
                - joueurs : une liste de tuples représentant les positions des joueurs de l'équipe 
                - ennemis : une liste de tuples représentant les positions des joueurs de l'équipe adverse   
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
                - jour : un entier représentant le numéro de la journée 
            * Si jour == 0 : alors cette stratégie applique la stratégie aléatoire à ses joueurs .
            * Sinon : 
                - D'abord, elle calcule le nombre de militants de l'équipe ennemis qui ont atteint leur électeur cible le jour précedent. Elle stocke dans un dictionnaire 
                "dico1" dont les clés sont les numéros des électeurs (selon l'ordre dans goalStates ), le nombre de militants de l'équipe adverse par élécteur.
                - A partir du dictionnaire "dico1", elle génère une liste "liste_ennemis" de taille nb_electeurs, et dont les valeurs sont le nombre de militants par électeur. On initilise une autre liste "liste_joueurs" de taille nb_electeurs et dont les valeurs seront mises à 0.
                - On ordonne les valeurs des militants par electeurs par odre croissant avec la fonction argsort. On prend les indices des 
                *** |k/2-1| *** électeurs qui ont le plus de militants, on affecte alors dans notre "liste_joueurs" à ces electeurs : nb_militants_equipe_advserse + 1.
                Par exemple , pour un electeur e dont l'indice est dans ceux des  *** |k/2-1| *** électeurs qui ont le plus de militants, on affectere
                *** liste_joueurs[e] = liste_ennemis[e] + 1 ***. On met 0 sur les autrs électeurs.
                - On vérifie bien que chaque militant a un electeur cible . Si ce n'est pas le cas *** (len(joueurs)-sum(liste_joueurs))!= 0 ***, alors on s'assure de  bien allouer à ces militants restants un électeur dans la liste goalStates.
                - Ensuite, on attribue à chaque electeur le nombre de militants qui lui ont été affectés. On crée une liste "goalStateJoueurs" qui attribuera aux *** liste_joueurs[e] *** miliants la position de l'électeur "goalStates[e]".
            * Pour résumer, cette stratégie s'assure donc que l'équipe des militants joueurs a posé une unité de plus que les militants adverses ont fait le jour précédent sur les (|K//2|) électeurs les plus  remplis.
        * *fictitious_play* :
            - Apprentissage : 
                * Prend en arguments :
                    - initStates : liste de couples représentants les positions initiales des joueurs
                    - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
                    - nb_jours   : entier représentant le nombre de jours que dure une compagne
                    - players    : liste des joueurs
                    - iterations : entier représentant le nombres d'itérations par jour.
                    - g          : matrice (grille) des postions contenant true si postion légale et false si on est sur un mur
                    - game       : une instance de jeu
                * Cette fonction fait jouer nos 02 équipes avec toutes les combinaisons de stratégies possibles en utilisant la fonction match expliquée ci-dessous . Elle génère une matrice des gains , qui stocke le gain cumulé d'un match entre deux stratégies s1 et s2. Nous avons considéré un jeu à somme nulle. Elle renvoie cette matrice des gains.
            - fictitious_play : 
                * Prend en arguments : 
                    - joueurs      : liste de tuples représentant les positions des militants de l'équipe 1
                    - ennemis      : liste de tuples représentant les positions des militants de l'équipe adverse
                    - goalStates   : une liste des positions des electeurs que l'on souhaite atteindre
                    - jour         : entier représentant le numéro du jour
                    - observations : liste représentant combien de fois une équipe a joué une stratégie au jour précédent (repésente notre prédiction à    priori)
                    - actions      : liste de tuples représentants toutes les combinaisons de stratégies possibles
                    - matGain      : matrice des gains renvoyée par la fonction apprentissage
                    - num_eq       : entier vaut 0 si c'est les joueurs qui jouent fictitious_play et 1 si c'est les ennemis
                - Nous considérons un modèle ou deux équipes sont en intéractions.
                - D'abord, elle calcule le nombre d'observations du jour précédent pour chaque équipe et les stocke dans une liste nbObservations.
                - Ensuite, pour chauqe action des militants de l'équipe joueur "myAction", elle récupère les actions de l'équipe adverse et calcule l'utilisteEsperée de myAction **observations[num_eq][myAction])/nbObservations[num_eq]*matGain[myAction][otherAction][num_eq]**
                - Elle va garder l'action myAction avec la plus grade utilité et l'élit comme meilleure action.
                - Elle fait jouer tous les joueurs de l'équipe joueur la stratégie correspondant à cette action avec la fonction jouer_stratégie.
                - Elle met à jour les observations , en ajoutant un à l'action choisit.
                - Elle renvoie les buts trouvés avec cette stratégie.
        * *Autre strategie* : 
            * *choix_strat_alea*:
                * Elle prend comme argument:
                    - joueurs      : liste de tuples représentant les positions des militants de l'équipe 1
                    - ennemis      : liste de tuples représentant les positions des militants de l'équipe adverse
                    - goalStates   : une liste des positions des electeurs que l'on souhaite atteindre
                    - jour         : entier représentant le numéro du jour
                * Elle choisit aléatoirement le nom d'une stratégie et applique celle-ci et renvoie les buts trouvés.

    * **utils.py** : qui contient le code des fonctions utiles qu'on utilise pour  :
        * *diviser_equipes* : 
            * prend en arguments :
                - initStates : la liste des positions initiales des joueurs (militants)
            * Cette fonction divise les joueurs en deux equipes , equipe paire et impaire, elle renvoie un tuple contenant deux listes des positions initiales des joueurs des deux équipes.
        * *regrouper_buts* :
            * prend en arguments :
                - buts1 : une liste des positions des élécteurs (goalStates) que les militants de l'équipe 1 souhaite atteindre
                - buts2 : une liste des positions des élécteurs (goalStates) que les militants de l'équipe 2 souhaite atteindre
            * Cette fonction regroupe les buts des deux équipes dans une seule liste en mettant les buts de l'équipe 1 aux indices paires et les buts de l'équipe 2 aux indices impaires.
        * *jouer_strategie* :
            * prend en arguments :
                - s : le nom de la stratégie à jouer
                - pos_joueur : une liste des positions joueurs d'une équipe
                - pos_ennemis : une liste des positions des joueurs de l'équipe adverse
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre       
                - jour : le numero du jour où on utilise la stratégie s
            * cette fonction fait appel à la stratégie ***s*** dont on passe le nom en paramètre et renvoie une liste des buts (positions d'électeurs) attribués aux militants en utilisant cette stratégie. 
        * *deplacement* :
            * prend en argument :
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
                - iterations : le nombre d'iterations à jouer par jour
                - posPlayers : une liste des positions courantes des joueurs (militants)
                - players : une liste des joueurs
                - paths : une liste contenant des listes des chemins partant de la position initiale du joueur vers la position de but pour chaque joueur 
                - buts : une liste des positions des élécteurs qu'on souhaite atteindre 
                - game : l'instance du jeu
            * Cette fonction permet le déplacement de tous les militants, chacun selon son path pour atteindre son électeur but pendant un nombre d'iterations précis. A chaque fois qu'un militant atteint son but, on verifie à quelle équipe il appartient et on stocke dans un dictionnaire pour chaque electeur le nombre de militants de l'équipe 1 et l'équipe 2 qui l'ont atteint et on renvoie ce dictionnaire. 
        * *match* :
            * prend en argument :
                - s_eq1 : le nom de la stratégie que va jouer l'équipe 1
                - s_eq2 : le nom de la stratégie que va jouer l'équipe 2
                - initStates : une liste des positions initiales des militans 
                - goalStates : une liste des positions des electeurs que l'on souhaite atteindre
                - nb_jours : le nombre de jours da la compagne
                - players : une liste des joueurs (militants)
                - iterations : le nombre d'itérations par jour
                - g : matrice (grille) des postions contenant true si postion légale et false si on est sur un mur
                - game : l'instance du jeu
            * Cette fonction représente le déroulement d'une __compagne sans budget de déplacement__ pendant ***nb_jours*** , elle fait jouer les deux équipes en utilisant la stratégie ***s_eq1*** pour l'équipe 1 et la stratégie ***s_eq2***  pour l'équipe 2 et en faisant appel à la fonction deplacement décrit ci-dessus. Chaque jour, on calcule le score de chaque équipe et on l'ajoute au score cumulé pour toute la compagne. A la fin de la compagne, on compare les scores cumulés pour chaque équipe et on met le gain de l'équipe gagnante à 1 et celui de l'équipe perdante à -1 et si aucune équipe a gagné, on met les gains des 2 équipes à 0 (jeu à somme nulle). Elle renvoie un tuple contenant les gains de chaque équipe.
        * *deplacement_budjet_v1* :
            * prend les memes arguments que la fonction déplacement ci-dessus en plus de l'argument:
                - budget : un nombre de pas de déplacement fixe pour chaque journée, pour chaque militant.
            * Cette fonction permet le déplacement de tous les militants, chacun selon son path pour atteindre son électeur but pendant un nombre d'iterations précis en considérant un ***budget fixe pour chaque journée***; __si le nombre de pas d'un militant atteint son budget, il arrete de se déplacer meme s'il n'a pas atteint son but__. 
            A chaque fois qu'un militant atteint son but, on verifie à quelle équipe il appartient et on stocke dans un dictionnaire pour chaque electeur le nombre de millitants de l'équipe 1 et l'équipe 2 qui l'ont atteint et on renvoie ce dictionnaire. 
        * *deplacement_budjet_v2* :
            * prend les memes arguments que la fonction déplacement ci-dessus en plus de l'argument:
                - budget : un nombre de pas de déplacement pour toute la compagne ; budget dynamique pour chaque journée.
            * Cette fonction permet le déplacement de tous les militants, chacun selon son path pour atteindre son électeur but pendant un nombre d'iterations précis en considérant un ***budget pour toute la compagne*** ; __chaque jour on soustrait de ce budget la somme des pas réalisés par les militants la journée précédente__. Une fois que le nombre de pas réalisés atteint ce budget, les militants arretent de se déplacer. 
            A chaque fois qu'un militant atteint son but, on verifie à quelle équipe il appartient et on stocke dans un dictionnaire pour chaque electeur le nombre de millitants de l'équipe 1 et l'équipe 2 qui l'ont atteint et on renvoie ce dictionnaire.          
        * *match_budget* :
            * prend les memes arguments que la fonction match ci-dessus en plus des deux arguments:
                - version : indique avec quelle version de déplacement il faut jouer :
                    - si version=1 on fait appel à la fonction deplacement_budget_v1 (budget fixe pour chaque journée)
                    - sinon on fait appel à la fonction deplacement_budget_v2 (budget pour toute la compagne; dynamique pour chaque journée)
                - budget : un nombre de pas de déplacement. Ca dépend de la version choisie:       
                    - si version=1 le budget vest un nombre de pas fixe pour chaque journée
                    - sinon le budget est un nombre de pas pour toute la compagne (dynamique pour chaque journée)
            * Cette fonction représente le déroulement d'une compagne __avec budget de déplacement__ pendant ***nb_jours***, elle fait jouer les deux équipes en utilisant la stratégie ***s_eq1*** pour l'équipe 1 et la stratégie ***s_eq2***  pour l'équipe 2 et en faisant appel à la fonction deplacement_budget_v1 ou  deplacement_budget_v2 . 
            En plus, pour ce jeu, __les électeurs sont réalloués au hasard dans de nouveaux secteurs chaque journée__ et donc chaque jour on change aléatoirement la liste des positions des élécteurs (goalStates).
            Chaque jour, on calcule le score de chaque équipe et on l'ajoute au score cumulé pour toute la compagne. A la fin de la compagne, on compare les scores cumulés pour chaque équipe et on met le gain de l'équipe gagnante à 1 et celui de l'équipe perdante à -1 et si aucune équipe a gagné, on met les gains des 2 équipes à 0 (jeu à somme nulle). Elle renvoie un tuple contenant les gains de chaque équipe.

    * **main.py** : fichiers ou l'on fait appel à toutes nos fonctions. Où l'on simule une compagne.
        * Pour tester notre, veuillez passer en paramètre le nombre d'itérations , le nom de la stratégie souhaitée pour l'équipe1 et 
        * le nom de la stratégie souhaitée pour l'équipe2.

## Description des résultats
* **Jeu Sans Budget**
    * En opposant aléatoire VS tetu : (resultat sur le graphe à trouver dans /doc/graphe_sansBudget/alea_tetu.png)
        - Score équipe 1 jouant avec la stratégie aléatoire est 7.
        - Score équipe 2 jouant avec la stratégie tetu est 6.
        * On remarque que aleatoire a un score supérieure à celui de tetu. Ce qui est normal car les joueurs de tetu jouent toujours la meme stratégie ,donc son gain dépendera des choix de l'autre équipe.   
    * En opposant tetu VS meilleureReponse : (resultat sur le graphe à trouver dans /doc/graphe_sansBudget/bestRep_tetu.png)
        - Score équipe 1 jouant avec la stratégie meilleureReponse 12
        - Score équipe 2 jouant avec la stratégie tetu est 9
        * On remarque que meilleure réponse a un score supérieure à celui de tétu. Ce qui est normal vu que tetu joue toujours la meme stratégie et meilleure réponse va répondre à cette stratégie. 
        Le score de tetu est à 9 car les militants ont atteint leurs buts comme ils ont toujours cette position et que les electeurs ne changent pas de position alors , ils remportent les electeurs.
    * En opposant stochastiqueExpert VS stochastiqueExpert: (resultat sur le graphe à trouver dans /doc/graphe_sansBudget/stocha_stocha.png)
        - Score équipe 1 jouant avec la stratégie stochastiqueExpert est 9
        - Score équipe 2 jouant avec la stratégie stochastiqueExpert est 12
        * On remarque que ce n'est pas le meme gain cumulé pour les deux équipes meme s'ils jouent tous les deux la strategie stochastiqueExpert, car cette strategie joue chaque jour une différente stratégie .  
    * En opposant fictitiousPlay VS meilleureReponse: (resultat sur le graphe à trouver dans /doc/graphe_sansBudget/fictitious_meilleureRep.png)
        - Score équipe 1 jouant avec la stratégie fictitiousPlay est 9
        - Score équipe 2 jouant avec la stratégie meilleureReponse est 7
        * On remarque que fictitoius Play a un score supérieur à celui de meilleureReponse. Ce qui est normal car fictitious Play choisit toujours la meilleure action à jouer en se basant sur les observations des jours précédents.   
    * En opposant choix_strat_alea VS tetu: (resultat sur le graphe à trouver dans /doc/graphe_sansBudget/fictitious_meilleureRep.png)
        - Score équipe 1 jouant avec la stratégie choix_strat_alea est 5
        - Score équipe 2 jouant avec la stratégie tetu est 4
        * On remarque que choix_start_alea a un score supérieur à celui de tetu. Car ici notre stratégie choix_strat_alea a choisi la stratégie aleatoire et comme on l'a expliqué précédemment celle gagne cotre tetu.
    * => On remarque qu'avec toutes ces stratégies nos militants atteignent leurs cibles car ils ne sont pas limités par un budget de déplacement
 * **Jeu avec Budget**
    * En opposant aléatoire VS tetu : (resultat sur le graphe à trouver dans /doc/graphe_avecBudget/alea_tetu.png)
        - Score équipe 1 jouant avec la stratégie aléatoire est 4
        - Score équipe 2 jouant avec la stratégie tetu est 3
       * On remarque que aleatoire a toujours un score supérieur à celui de tetu. Ce qui est normal car les joueurs de tetu jouent toujours la meme stratégie , mais on remarque que les scores avec aleatoire et tetu sont inferieurs aux scores trouvés en jouant sans budget de deplacement, car certains militants n'atteignent pas leurs buts à cause de la contrainte de budget . 
    * En opposant tetu VS meilleureReponse : (resultat sur le graphe à trouver dans /doc/graphe_avecBudget/bestRep_tetu.png)
        - Score équipe 1 jouant avec la stratégie meilleureReponse est 2
        - Score équipe 2 jouant avec la stratégie tetu est 3
        * On remarque que meilleure réponse a un score inférieur à celui de tétu. Ce qu'on peut expliquer par le fait que meilleureReponse choisit la meilleure réponse à la stratégie de l'équipe adversaire du jour précédent, et ici malgré le fait que ce soit une stratégie tétu , elle ne peut pas choisir la meilleure réponse car les électeurs vont changer de places au jour suivant (elle ne prédit pas le changement de places). Donc meilleureReponse est une stratégie qui s'adapte mieux aux environnements statiques.      
    * En opposant stochastiqueExpert VS stochastiqueExpert: (resultat sur le graphe à trouver dans /doc/graphe_avecBudget/stocha_stocha.png)
        - Score équipe 1 jouant avec la stratégie stochastiqueExpert est 6
        - Score équipe 2 jouant avec la stratégie stochastiqueExpert est 4
        * On remarque que ce n'est pas le meme gain cumulé pour les deux équipes meme s'ils jouent tous les deux la strategie stochastiqueExpert, car cette strategie joue chaque jour une différente stratégie . 
        Le gain cumulé est inférieur à celui trouvé sans budget, car certains militants n'atteignent pas leurs cibles à cause de la contrainte de budget.
    * En opposant fictitiousPlay VS meilleureReponse: (resultat sur le graphe à trouver dans /doc/graphe_avecBudget/fictitious_meilleureRep.png)
        - Score équipe 1 jouant avec la stratégie fictitiousPlay est 10
        - Score équipe 2 jouant avec la stratégie meilleureReponse est 6
        * On remarque que fictitoius Play a un score supérieure à celui de meilleureReponse. Ce qui est normal car fictitious Play choisit toujours la meilleure action à jouer en se basant sur les observations des jours précédents.   
    * => On remarque quue nos militants peuvent ne pas atteindre leurs cibles car ils sont limités par un budget de déplacement fixe par jour.