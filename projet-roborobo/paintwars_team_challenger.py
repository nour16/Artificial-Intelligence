# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Melina BESSAD
#  Prénom Nom: NourElHouda KLICH

from pyroborobo import Pyroborobo, Controller, AgentObserver, WorldObserver, CircleObject, SquareObject, MovableObject
# from custom.controllers import SimpleController, HungryController
import numpy as np
import random
import paintwars_arena

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors

def get_team_name():
    return "The Great Challengers" 
    
def loveBot(robotId, sensors):
    """fonction permettant de suivre les robots"""
    translation = (-1) * sensors["sensor_front"]["distance_to_robot"] 
    rotation = (1)*sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance_to_robot"]
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation


def hateBot(robotId, sensors):
    """fonction permettant d'éviter les robots"""
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]#-1 va a gauche et 1 a droite
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation


def hateWall(robotId, sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_wall"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"]["distance_to_wall"]
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation



def braitenberg_comportement(robotId, sensors):
    ##suivre nos ennemis
    if ((sensors["sensor_front"]["isRobot"]==True and sensors["sensor_front"]["isSameTeam"] == False) or 
        (sensors["sensor_front_left"]["isRobot"]==True and sensors["sensor_front_left"]["isSameTeam"] == False) or 
        (sensors["sensor_front_right"]["isRobot"]==True and sensors["sensor_front_right"]["isSameTeam"] == False)):

        translation, rotation =  loveBot(robotId, sensors)
    ##eviter les coequipiers
    elif (( sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True) or 
          ( sensors["sensor_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == True) or 
          ( sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == True)):
        translation, rotation = hateBot(robotId, sensors)
    ##si on a des murs
    elif (sensors["sensor_front"]["distance_to_wall"] < 1 or sensors["sensor_front_left"]["distance_to_wall"]<1 or sensors["sensor_front_right"]["distance_to_wall"]<1):
        translation, rotation =  hateWall(robotId, sensors)
        if (sensors["sensor_front_left"]["distance_to_wall"]==sensors["sensor_front_right"]["distance_to_wall"]):
            rotation = 0.5
    return translation, rotation

def comportement_defaut(robotID, sensors):

    rotation = 0
    translation = 1

    if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
        rotation = 0.5
    elif sensors["sensor_front_right"]["distance"] < 1:
        rotation = -0.5 

    return translation, rotation

def step(robotId, sensors):
    
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)
    sensors  = get_extended_sensors(sensors)

    # initialisation
    enemy_detected_by_front_sensor = False
    enemy_detected_by_front_right_sensor = False
    enemy_detected_by_front_left_sensor = False
    enemy_detected_by_right_sensor = False
    enemy_detected_by_left_sensor = False
    enemy_detected_by_back_sensor = False
    enemy_detected_by_back_right_sensor = False
    enemy_detected_by_back_left_sensor = False

    ally_detected_by_front_sensor = False
    ally_detected_by_front_right_sensor = False
    ally_detected_by_front_left_sensor = False
    ally_detected_by_right_sensor = False
    ally_detected_by_left_sensor = False

    wall_detected_left = False
    wall_detected_right = False
    wall_detected_front = False
    wall_detected_front_right = False
    wall_detected_front_left = False
    wall_detected_back_right = False
    wall_detected_back_left = False
    wall_detected_back = False
    # détection d'un robot de l'équipe adversaire
    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
        enemy_detected_by_front_sensor = True
    if sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == False:
        enemy_detected_by_front_right_sensor = True
    if sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == False:
        enemy_detected_by_front_left_sensor = True
    if sensors["sensor_right"]["isRobot"] == True and sensors["sensor_right"]["isSameTeam"] == False:
        enemy_detected_by_right_sensor = True
    if sensors["sensor_left"]["isRobot"] == True and sensors["sensor_left"]["isSameTeam"] == False:
        enemy_detected_by_left_sensor = True
    if sensors["sensor_back"]["isRobot"] == True and sensors["sensor_back"]["isSameTeam"] == False:
        enemy_detected_by_back_sensor = True
    if sensors["sensor_back_right"]["isRobot"] == True and sensors["sensor_back_right"]["isSameTeam"] == False:
        enemy_detected_by_back_right_sensor = True
    if sensors["sensor_back_left"]["isRobot"] == True and sensors["sensor_back_left"]["isSameTeam"] == False:
        enemy_detected_by_back_left_sensor = True

    # détection d'un robot de la même équipe
    if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True:
        ally_detected_by_front_sensor = True
    if sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == True:
        ally_detected_by_front_right_sensor = True
    if sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == True:
        ally_detected_by_front_left_sensor = True
    if sensors["sensor_right"]["isRobot"] == True and sensors["sensor_right"]["isSameTeam"] == True:
        ally_detected_by_right_sensor = True
    if sensors["sensor_left"]["isRobot"] == True and sensors["sensor_left"]["isSameTeam"] == True:
        ally_detected_by_left_sensor = True

    # détection des murs
    if sensors["sensor_left"]["distance"] < 1 and sensors["sensor_left"]["isRobot"] == False:
        wall_detected_left = True
    if sensors["sensor_right"]["distance"] < 1 and sensors["sensor_right"]["isRobot"] == False:
        wall_detected_right = True
    if sensors["sensor_front"]["distance"] < 1 and sensors["sensor_front"]["isRobot"] == False:
        wall_detected_front = True
    if sensors["sensor_front_right"]["distance"] < 1 and sensors["sensor_front_right"]["isRobot"] == False:
        wall_detected_front_right = True
    if sensors["sensor_front_left"]["distance"] < 1 and sensors["sensor_front_left"]["isRobot"] == False:
        wall_detected_front_left = True
    if sensors["sensor_back_right"]["distance"] < 1 and sensors["sensor_back_right"]["isRobot"] == False:
        wall_detected_back_right = True
    if sensors["sensor_back_left"]["distance"] < 1 and sensors["sensor_back_left"]["isRobot"] == False:
        wall_detected_back_left = True
    if sensors["sensor_back"]["distance"] < 1 and sensors["sensor_back"]["isRobot"] == False:
        wall_detected_back = True

   
   
    

    # suivre les ennemis
    if enemy_detected_by_front_sensor:
        rotation = 0
    elif enemy_detected_by_front_right_sensor:
        rotation = 0.25
    elif enemy_detected_by_front_left_sensor:
        rotation = -0.25
    elif enemy_detected_by_right_sensor:
        rotation = 0.5
    elif enemy_detected_by_left_sensor:
        rotation = -0.5
    elif enemy_detected_by_back_sensor:
        rotation = 1
    elif enemy_detected_by_back_right_sensor:
        rotation = 0.75
    elif enemy_detected_by_back_left_sensor:
        rotation = -0.75

     # évite les alliés
    elif ally_detected_by_right_sensor:
        rotation = -0.5
    elif ally_detected_by_left_sensor :
        rotation = 0.5
    elif ally_detected_by_front_right_sensor:
        rotation = -0.5
    elif ally_detected_by_front_left_sensor:
        rotation = 0.5
    elif ally_detected_by_front_sensor and not( wall_detected_left  or wall_detected_right) :
        rotation = 1
    elif ally_detected_by_front_sensor  and( wall_detected_left  or wall_detected_right):
        translation = -1
        rotation = 1
    
   
    #Gestion des murs 
         
    elif (wall_detected_front and wall_detected_front_right) or (wall_detected_right and wall_detected_front_right):
        rotation = -0.5
    elif (wall_detected_front and wall_detected_front_left) or (wall_detected_left and wall_detected_front_left):
        rotation = 0.5
    elif wall_detected_front_right:
        rotation = -0.25
    elif  wall_detected_front_left or wall_detected_front:
        rotation = 0.25
    
    elif not wall_detected_front_left and  wall_detected_left and not wall_detected_back_left: #longe les murs et rentre si il y a une ouverture à gauche
        rotation = -0.25
    elif not wall_detected_front_left and  wall_detected_left :#permet d'eviter le blocage 
        rotation = 0.25
    elif not wall_detected_front_right and  wall_detected_right and not wall_detected_back_right: #longe les murs et rentre si il y a une ouverture à droite
        rotation = 0.25
    elif not wall_detected_front_right and  wall_detected_right :#permet d'eviter le blocage
        rotation = -0.25

    elif  (wall_detected_right and wall_detected_back_right):
        rotation = -0.25     
    elif (wall_detected_left and wall_detected_back_left):    
        rotation = 0.25      
    elif (wall_detected_left):
        rotation = 0.25
    elif (wall_detected_right):
        rotation = -0.25
    

    
           
    return translation, rotation