from ctypes import util
import random
from re import M 
import numpy as np
import utils
STRATEGIES = ["aleatoire","tetu","meilleureReponse","StochastiqueExpert",]


##############StrategieAleatoire############
def aleatoire(players,goalStates):
    """attribue a chaque militant un electeur aleatoirement"""
    return [random.choice(goalStates) for p in range(len(players))]


# ##############StrategieTetu############
def tetu(players,goalStates):
    return [goalStates[i%len(goalStates)] for i in range(len(players)) ]

###############StochastiqueExpert############
def StochastiqueExpert(joueurs,ennemis,goalStates,jour,strategies=[s for s in STRATEGIES if s!="StochastiqueExpert"]):
    proba_strat = [random.random() for i in range(len(strategies))]#on va faire correspondre a chaque strategie une probabilité
    p = random.random()
    idx_strat = np.argmin([abs(proba-p) for proba in proba_strat]) #on choisit la strategie dont la probabilité p se rapproche le plus de p
    buts  = utils.jouer_strategie(strategies[idx_strat],joueurs,ennemis,goalStates,jour)
    return buts


###############MeilleureReponse############
def meilleureReponse(joueurs,ennemis,goalStates,jour):
    if jour==0:#le premier jour le joueur joue une strategie aleatoire 
        return aleatoire(joueurs, goalStates)    
    #les autres jours il fait meilleure reponse
    dico1 = dict(zip([j for j in range(len(goalStates))],[0 for j in range(len(goalStates))]))#dico associant chaque electeur au nombre de militants de ennemis
    for i in range(len(goalStates)):
        for j in range(len(ennemis)):
            if goalStates[i]==ennemis[j]:#le joueur j a atteint sa cible
                dico1[i]+=1
    liste_ennemis = [v for (k,v) in dico1.items()]#liste du nombre de militants pour chaque electeur
    liste_joueurs = [0 for i in range(len(goalStates))]
    idx = np.argsort(liste_ennemis)
    
    #laisser les derniers |k/2-1| les plus remplis des ennemis
    for i in idx[:len(ennemis)//2]:#rajouter une unite les moins remplis des ennemis
        liste_joueurs[i] = liste_ennemis[i] + 1
    #on verifie de bien allouer tous les militants 
    nb_militants_restants = len(joueurs)-sum(liste_joueurs)
    while(nb_militants_restants!=0):
        for i in range(len(liste_joueurs)):
            if nb_militants_restants==0:
                break
            liste_joueurs[i]+=1
            nb_militants_restants-=1
    #attribuer des electeurs aux militants
    goalStateJoueurs = []
    for i in range(len(liste_joueurs)):
        nb_militants = liste_joueurs[i]
        for j in range(nb_militants):
            goalStateJoueurs.append(goalStates[i])
    return goalStateJoueurs   #on retourne les objectifs des joueurs 





##############fictitious play##############
def apprentissage(initStates, goalStates, nb_jours, players, iterations,g,game):
    matGain= dict(zip([s for s in STRATEGIES],[dict() for s in STRATEGIES]))
    for s in STRATEGIES:
        matGain[s] = dict(zip([s for s in STRATEGIES],[(0,0) for s in range(len(STRATEGIES))]))
    for s1 in STRATEGIES:
        for s2 in STRATEGIES:
            matGain[s1][s2] = utils.match(s1,s2,initStates,goalStates,nb_jours,players,iterations,g,game)

    return matGain

def fictitious_play(joueurs,ennemis,goalStates,jour,observations,actions,matGain,num_eq):
    nbObservations = [sum (observations[i].values()) for i in range(2)]
    utiliteEsperee = dict(zip([s for s in STRATEGIES],[0 for s in range(len(STRATEGIES))]))
    bestAction = actions[0][0]
    bestGain = 0
    if num_eq==0: num_eq2 =1
    else : num_eq2=0
    for myAction in actions[num_eq]:
        for otherAction in actions[num_eq2]:
            utiliteEsperee[myAction] += (observations[num_eq][myAction])/nbObservations[num_eq]*matGain[myAction][otherAction][num_eq]
        if utiliteEsperee[myAction]>bestGain:
            bestAction = myAction
            bestGain = utiliteEsperee[myAction]    
    return (utils.jouer_strategie(bestAction,joueurs,ennemis,goalStates,jour),bestAction)



###############AutresStrategies############ 
def choix_strat_alea(joueurs,ennemis,goalStates,jour):
    " on choisit une stratégie aléatoirement"
    strat = random.choice(STRATEGIES)
    print("---------------------------choix_strtat_alea choisit la strategie "+strat+"------------------")
    return utils.jouer_strategie(strat,joueurs,ennemis,goalStates,jour)