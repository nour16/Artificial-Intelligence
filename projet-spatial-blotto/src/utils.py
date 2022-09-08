
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


def diviser_equipes(initStates):
    """divise les joueurs en deux équipes ; equipe paire et impaire"""
    return ([initStates[i] for i in range(len(initStates)) if i%2],[initStates[i] for i in range(len(initStates)) if (i%2!=0)])

def regrouper_buts(buts1,buts2):
    buts = []
    for i in range(len(buts1+buts1)):
        #on ajoute les buts a tour de role (pair /impair)
        if i%2:
            buts.append(buts1[i//2])
        else :
            buts.append(buts2[i//2])
    return buts

def jouer_strategie(s,pos_joueur,pos_ennemis,goalStates,jour):
    """
        cette fonction prend en paramètre le nom de la stratégie s qu'on souhaite utiliser
        Elle y fait appel et renvoie les buts
    """
    buts = []
    if (s=="aleatoire"):
        buts  = strategie.aleatoire(pos_joueur,goalStates)
    elif (s=="tetu"):
        buts = strategie.tetu(pos_joueur,goalStates)
    elif (s == "meilleureReponse"):
        buts = strategie.meilleureReponse(pos_joueur,pos_ennemis,goalStates,jour)
    elif (s=="StochastiqueExpert"):
        buts = strategie.StochastiqueExpert(pos_joueur,pos_ennemis,goalStates,jour)
    else:
        buts = strategie.choix_strat_alea(pos_joueur,pos_ennemis,goalStates,jour)
    return buts

def deplacement(goalStates,iterations,posPlayers,players,paths,buts,game):
        nbMiliElec = dict(zip([j for j in goalStates],[[0,0] for j in range(len(goalStates))])) #pour chaque electeur on a le nb de millitants pour equipe1 et equipe2
        players_winners = []#liste des joueurs ayant trouvé leur but
        for i in range(iterations):
            if len(players_winners)==len(players):#si tous les joueurs ont atteint leurs objectifs
                break
            for j in range(len(players)):
                # on fait bouger chaque joueur séquentiellement
                # Joeur j: suit son chemin trouve avec A* 
                path = paths[j]
                if j not in players_winners:
                    row,col = path[i]
                    posPlayers[j]=(row,col)
                    players[j].set_rowcol(row,col)
                    #print ("pos ",j,":", row,col)
                    if( (row,col) == buts[j]):
                        if j%2==0:
                            nbMiliElec[buts[j]][0]+=1
                        else:
                            nbMiliElec[buts[j]][1]+=1

                        players_winners.append(j)   
                        #print("le joueur ",j," a atteint son but!")
                       
            game.mainiteration()
        return nbMiliElec


def match(s_eq1,s_eq2,initStates,goalStates,nb_jours,players,iterations,g,game):
    """renvoie le gain cumule pour tous les jours"""
    (pos_e1,pos_e2) = diviser_equipes(initStates)
    S1=[]
    S2=[]
    tmpStates = initStates 
    score_eq1 = 0
    score_eq2 = 0
    for jour in range(nb_jours):
        paths=[]
        #faire appel aux strategies
        buts1 = jouer_strategie(s_eq1,pos_e1,pos_e2,goalStates,jour)
        buts2 = jouer_strategie(s_eq2,pos_e2,pos_e1,goalStates,jour)
        #regrouper les buts pour le jeu (en gardant faisant attention aux indices de depart)
        buts = regrouper_buts(buts1,buts2)
        for pl in range(len(initStates)):
            p = ProblemeGrid2D(tmpStates[pl],buts[pl],g,'manhattan')
            path = probleme.astar(p)
            paths.append(path)
        # Boucle principale de deplacements 
        score_equipe={1:0,2:0}
        nbMiliElec=deplacement(goalStates,iterations,tmpStates,players,paths,buts,game)
        #calculer le score par jour des equipes
        for c,[v1,v2] in nbMiliElec.items():
            if v1>v2 : score_equipe[1]+=1
            elif v1<v2 :  score_equipe[2]+=1
        score_eq1 += score_equipe[1]
        score_eq2 += score_equipe[2]
        print("Le score des 02 equipes pour le jour",jour," : ",score_equipe)
        gain_eq1=0
        gain_eq2=0
        if score_eq1>score_eq2: 
            gain_eq1=1
            gain_eq2=-1
        elif score_eq1<score_eq2: 
            gain_eq1=-1
            gain_eq2=1
        S1.append(score_eq1)
        S2.append(score_eq2)
    print("Le score cumule pour equipe1 en jouant la strategie ",s_eq1," est : ",score_eq1)
    print("Le score cumule pour equipe2 en jouant la strategie ",s_eq2," est : ",score_eq2)
    plt.plot([j for j in range(nb_jours)],S1,color='red',label="equipe1 jouant la strategie "+s_eq1)
    plt.plot([j for j in range(nb_jours)],S2,color='blue',label="equipe2 jouant la strategie "+s_eq2)
    plt.title("Score cumule pour les 2 equipes pendant "+str(nb_jours))
    plt.xlabel("jour")
    plt.xlabel("score")
    plt.legend()
    plt.show()
    return (gain_eq1,gain_eq2)
##################DeplacementABudgetFixe########################################
def deplacement_budjet_v1(goalStates,iterations,posPlayers,players,paths,buts,game,budget):
        nbMiliElec = dict(zip([j for j in goalStates],[[0,0] for j in range(len(goalStates))])) #pour chaque electeur on a le nb de millitants pour equipe1 et equipe2
        players_winners = []#liste des joueurs ayant trouvé leur but
        nb_pas=[0 for i in range(len(players))]
        for i in range(iterations):
            if len(players_winners)==len(players):#si tous les joueurs ont atteint leurs objectifs
                break
            for j in range(len(players)):
                # on fait bouger chaque joueur séquentiellement
                # Joeur j: suit son chemin trouve avec A* 
                path = paths[j]
                if j not in players_winners :
                    nb_pas[j]=nb_pas[j]+1
                    row,col = path[i]
                    posPlayers[j]=(row,col)
                    players[j].set_rowcol(row,col)
                    #print ("pos ",j,":", row,col)
                    if( (row,col) == buts[j]):
                        if j%2==0:
                            nbMiliElec[buts[j]][0]+=1
                        else:
                            nbMiliElec[buts[j]][1]+=1
                        players_winners.append(j)   
                        #print("le joueur ",j," a atteint son but!")
                if nb_pas[j] >= budget:
                    break
            if nb_pas[j]>= budget:#si il finit son budget on break
                break
            game.mainiteration()
        return nbMiliElec

##################DeplacementABudgetDynamique########################################
def deplacement_budjet_v2(goalStates,iterations,posPlayers,players,paths,buts,game,budget):
        nbMiliElec = dict(zip([j for j in goalStates],[[0,0] for j in range(len(goalStates))])) #pour chaque electeur on a le nb de millitants pour equipe1 et equipe2
        players_winners = []#liste des joueurs ayant trouvé leur but
        nb_pas=[0 for i in range(len(players))]
        for i in range(iterations):
            if len(players_winners)==len(players):#si tous les joueurs ont atteint leurs objectifs
                break
            for j in range(len(players)):
                # on fait bouger chaque joueur séquentiellement
                # Joeur j: suit son chemin trouve avec A* 
                path = paths[j]
                if j not in players_winners and nb_pas[j]<budget:
                    nb_pas[j]=nb_pas[j]+1
                    row,col = path[i]
                    posPlayers[j]=(row,col)
                    players[j].set_rowcol(row,col)
                    #print ("pos ",j,":", row,col)
                    if( (row,col) == buts[j]):
                        if j%2==0:
                            nbMiliElec[buts[j]][0]+=1
                        else:
                            nbMiliElec[buts[j]][1]+=1
                        players_winners.append(j)   
                        #print("le joueur ",j," a atteint son but!")
                if nb_pas[j] >= budget:
                    break
            if nb_pas[j]>= budget:#si il finit son budget on break
                break 
            game.mainiteration()
        budget -= sum(nb_pas)
        return nbMiliElec


  
def match_budget(s_eq1,s_eq2,initStates,goalStates,nb_jours,players,iterations,g,game,budget,version):
    """renvoie le gain cumule pour tous les jours"""
    (pos_e1,pos_e2) = diviser_equipes(initStates)
    tmpStates = initStates 
    score_eq1 = 0
    score_eq2 = 0
    liste_pos=[]
    S1=[]
    S2=[]
    states=[o for o in game.layers['ramassable']]
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] : liste_pos.append((i,j))
    print("-----------------LA COMPAGNE EST LANCEE------------------------")
    for jour in range(nb_jours):
        paths=[]
        #faire appel aux strategies
        buts1 = jouer_strategie(s_eq1,pos_e1,pos_e2,goalStates,jour)
        buts2 = jouer_strategie(s_eq2,pos_e2,pos_e1,goalStates,jour)
        #regrouper les buts pour le jeu (en gardant faisant attention aux indices de depart)
        buts = regrouper_buts(buts1,buts2)
        for pl in range(len(initStates)):
            p = ProblemeGrid2D(tmpStates[pl],buts[pl],g,'manhattan')
            path = probleme.astar(p)
            paths.append(path)
        # Boucle principale de deplacements 
        score_equipe={1:0,2:0}
        if version==1:#version avec budget fixe
            nbMiliElec=deplacement_budjet_v1(goalStates,iterations,tmpStates,players,paths,buts,game,budget)
        else :#avec budget dynamique
            nbMiliElec=deplacement_budjet_v2(goalStates,iterations,tmpStates,players,paths,buts,game,budget)
        #calculer le score par jour des equipes
        for c,[v1,v2] in nbMiliElec.items():
            if v1>v2 : score_equipe[1]+=1
            elif v1<v2 :  score_equipe[2]+=1
        score_eq1 += score_equipe[1]
        score_eq2 += score_equipe[2]
        print("Le score des 02 equipes pour le jour",jour+1," : ",score_equipe)
        gain_eq1=0
        gain_eq2=0
        if score_eq1>score_eq2: 
            gain_eq1=1
            gain_eq2=-1
        elif score_eq1<score_eq2: 
            gain_eq1=-1
            gain_eq2=1
        S1.append(score_eq1)
        S2.append(score_eq2)
        #reallocation des emplacements des goalstates (electeurs)
        for i in range(len(goalStates)):
            (row,col)=random.choice(liste_pos)
            goalStates[i]=((row,col))
            states[i].set_rowcol(row,col)
    print("Le score cumule pour equipe1 en jouant la strategie ",s_eq1," est : ",score_eq1)
    print("Le score cumule pour equipe2 en jouant la strategie ",s_eq2," est : ",score_eq2)
    plt.plot([j for j in range(nb_jours)],S1,color='red',label="equipe1 jouant la strategie "+s_eq1)
    plt.plot([j for j in range(nb_jours)],S2,color='blue',label="equipe2 jouant la strategie "+s_eq2)
    plt.title("Score cumule pour les 2 equipes pendant "+str(nb_jours))
    plt.xlabel("jour")
    plt.xlabel("score")
    plt.legend()
    plt.show()
    return (gain_eq1,gain_eq2)