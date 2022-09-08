Stratégie adoptée:  
    
On a utilisé une architecture de subsomption pour implémenter les différents        comportements de nos robots et les organiser par ordre de priorités.

* Ci-dessous les comportements par ordre de priorités ( 1 étant la plus grande priorité et 4 la plus petite).

    * Comportement 1 :  Suivre les adversaire
     -> Grâce aux six capteurs disposés sur le robot, nous pouvons calculer la distance qui nous sépare de nos ennemis. Si un capteur détecte un ennemi à moins de 1 de distance alors on fait une rotation dans la direction de celui-ci et on le suit.

    * Comportement 2 :  Eviter les alliés
     -> Grâce aux six capteurs disposés sur le robot, nous pouvons calculer la distance qui nous sépare de nos ennemis aussi. Si un capteur détecte un allié à moins de 1 de distance alors on fait une rotation à l’inverse de sa  position dans le but de s’éloigner de lui et d’éviter les inter-blocages entre robots d’une même équipe.

    * Comportement 3 :  Gestion des murs 
     -> Toujours avec les capteurs, ils longent les murs et si il y a une petite ouverture le long de celui-ci alors les robots la prennent. Pour ne pas avoir des robots uniquement collés au murs, nous avons fait en sorte de les écarter des murs afin de leurs permettre de remplir plus d’espaces.

    * *Comportement 4 :  Aller tout droit
     -> Si aucune des conditions n’est réalisée pour appliquer l’un des comportement au-dessus , alors les robots appliquent un comportement par défaut qui leur permet d’aller tout droit.  
