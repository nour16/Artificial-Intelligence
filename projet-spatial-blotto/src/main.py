# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals
import operator
import random 
import numpy as np
import sys
from itertools import chain
import pygame
import matplotlib.pyplot as plt


from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo
import strategie 
from search.grid2D import ProblemeGrid2D
from search import probleme
import utils



# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player



def main():
    nb_jours = 5
    #for arg in sys.argv:
    iterations = 100# default
    strat1="aleatoire"
    strat2="tetu"
    if len(sys.argv) >= 2:
        iterations = int(sys.argv[1])
        strat1=sys.argv[2]   
        strat2=sys.argv[3]

    print ("Iterations: ")
    print (iterations)

    init()
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
       
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    print ("Init states:", initStates)
    
    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    
        
    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
    
    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols
     
    g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True  
    for w in wallStates:            # putting False for walls
        g[w]=False
    
    budget = 8

     ##          Test d'un match sans budget
    (g_eq1,g_eq2)= utils.match(strat1,strat2,initStates,goalStates,nb_jours,players,iterations,g,game)

    ##          Test d'un match avec budget statique
    #(g_eq1,g_eq2)=utils.match_budget(strat1,strat2,,initStates,goalStates,nb_jours,players,iterations,g,game,budget,1)

    ##          Test d'un match avec budget dynamique
    #(g_eq1,g_eq2)=utils.match_budget(strat1,strat2,initStates,goalStates,nb_jours,players,iterations,g,game,budget,2)

    if g_eq1>g_eq2 :
        print("Equipe 1 a remporté la compagne")
    elif g_eq1 < g_eq2:
        print("Equipe 2 a remporté la compagne")
    else:
        print("Aucune équipe n'a gagné")

    """##            fictious play
    mat_Gain  = strategie.apprentissage(initStates, goalStates, nb_jours, players, iterations,g,game)#renvoie la matrice des gain
    print(mat_Gain)
    actions = []
    #for j in range(nbPlayers//2):
       
    for s1 in strategie.STRATEGIES:
        for s2 in strategie.STRATEGIES : 
            actions.append((s1,s2))
        #actions.append(actions_j)
    
    ##initialisation des observations
    observations = []
    for j in range(2):
        observations.append(dict(zip([s for s in strategie.STRATEGIES],[1 for s in strategie.STRATEGIES])))
    (pos_e1,pos_e2) = utils.diviser_equipes(initStates)
    tmpStates = initStates 
    score_eq1 = 0
    score_eq2 = 0
    S1=[]
    S2=[]
    for jour in range(nb_jours):
        paths=[]
        #faire appel aux stratégies
        num_eq_ficti = 1
        (buts1,nextAction) = strategie.fictitious_play(pos_e1,pos_e2,goalStates,jour,observations,actions,mat_Gain,num_eq_ficti)#on recupere les affectations des militants et les actions choisies
        #buts2 = strategie.StochastiqueExpert(pos_e2,pos_e1,goalStates,jour)
        buts2 = utils.jouer_strategie("meilleureReponse",pos_e2,pos_e1,goalStates,jour)
        ##      Mise à jour des observations
        for s,v in observations[num_eq_ficti].items():
            if s == nextAction :
                v +=1

        #regrouper les buts pour le jeu (en gardant faisant attention aux indices de départ)
        print('-----------------------------------------------------',buts2)
        buts = utils.regrouper_buts(buts1,buts2)
        for pl in range(len(initStates)):
            p = ProblemeGrid2D(tmpStates[pl],buts[pl],g,'manhattan')
            path = probleme.astar(p)
            paths.append(path)
        # Boucle principale de déplacements 
        score_equipe={1:0,2:0}
        nbMiliElec=utils.deplacement(goalStates,iterations,tmpStates,players,paths,buts,game)
        #calculer le score par jour des equipes
        for c,[v1,v2] in nbMiliElec.items():
            if v1>v2 : score_equipe[1]+=1
            elif v1<v2 :  score_equipe[2]+=1
        
        score_eq1 += score_equipe[1]
        score_eq2 += score_equipe[2]
        S1.append(score_eq1)
        S2.append(score_eq2)
    print("Le score cumule pour equipe1 en jouant la strategie fictitious est : ",score_eq1)
    print("Le score cumule pour equipe2 en jouant la strategie meilleureReponse est : ",score_eq2)
    plt.plot([j for j in range(nb_jours)],S1,color='red',label="equipe1 jouant la strategie fictitious_play")
    plt.plot([j for j in range(nb_jours)],S2,color='blue',label="equipe2 jouant la strategie meilleure_reponse")
    plt.title("Score cumule pour les 2 equipes pendant "+str(nb_jours))
    plt.xlabel("jour")
    plt.xlabel("score")
    plt.legend()
    plt.show()
 
"""
    pygame.quit()
    
    
    
    
   

if __name__ == '__main__':
    main()
    


