"""Module for robot movement functions."""
from controller import Controller
import numpy as np
import time

def bouger(controller : Controller, distance : int, vitesse : int):
    """Fait bouger le robot d'une distance donnée en cm."""
    impulsions = distance * 160  # 160 impulsions par cm voir test avancer_test.py
    controller.set_motor_speed(vitesse, vitesse)
    controller.get_encoder_ticks()
    ticks_left = 0
    ticks_right = 0

    while True:
        current_ticks = controller.get_encoder_ticks()
        ticks_left += current_ticks[0]
        ticks_right += current_ticks[1]
        if (ticks_left * vitesse/abs(vitesse) >= impulsions or ticks_right * vitesse/abs(vitesse) >= impulsions):
            break

    controller.standby()

def avancer(controller : Controller, distance : int):
    """Fait avancer le robot d'une distance donnée en cm."""
    bouger(controller, distance, 50)

def arriere(controller : Controller, distance : int):
    """Fait reculer le robot d'une distance donnée en cm."""
    bouger(controller, distance, -50)
def tourner(controller : Controller, sens : int):
    """Fait tourner le robot à droite de 15 degrés. (sens = 1 pour droite, -1 pour gauche)"""
    controller.set_motor_shutdown_timeout(5)
    controller.set_motor_speed(50 * sens, -50 * sens)
    controller.get_encoder_ticks()
    impulsions = 200  # 200 impulsions pour un tour de 15 degrés (testé empiriquement)
    ticks_left = 0
    ticks_right = 0

    while True:
        current_ticks = controller.get_encoder_ticks()
        ticks_left += current_ticks[0]
        ticks_right += current_ticks[1]
        if (ticks_left * sens >= impulsions) or (ticks_right * -sens >= impulsions):
            break

    controller.standby()

def tourner_droite(controller : Controller):
    """Fait tourner le robot à droite de 15 degrés."""
    tourner(controller, 1)

def tourner_gauche(controller : Controller):
    """Fait tourner le robot à gauche de 15 degrés."""
    tourner(controller, -1)

def danse(controller : Controller, sens : int = 1):
    for _ in range(36):
        if sens == 1:
            tourner_droite(controller)
        else:
            tourner_gauche(controller)

def calcul_distance (ticks):
        dist= (ticks/(120*8*4))*6.5*3.14
        return dist

def calcul_ticks (distance): #en cm
    ticks=(distance/(6.5*3.14))*120*8*4
    return np.floor(ticks)


def reculer_alternatif(controller : Controller, distance : int):
    ticks_max=calcul_ticks(distance)

    Kp = 0.5
    Ki = 0.5
    Kd = 0

    speed_g=-90 # ne surtout pas modifier
    ecart=-2 # ne surtout pas modifier
    speed_d=speed_g-ecart # ne surtout pas modifier
    controller.set_raw_motor_speed(speed_g, speed_d)
    print("Initilisation Moteur ok")

    integrale = 0
    prev_error = 0

    total_ticks=0

    while total_ticks < ticks_max-1000:

        # Lire la vitesse réelle des moteurs
        speeds = controller.get_raw_motor_speed()
        if speeds is None:
            continue
        speed_g, speed_d = speeds

        # Erreur
        error = speed_g - (speed_d-ecart) + 0.1

        # PID
        integrale += error
        derivative = error - prev_error
        prev_error = error
        correction = Kp*error + Ki*integrale + Kd*derivative

        # Appliquer la correction dans le bon sens

        speed_g = speed_g - correction 
        speed_d = speed_d + correction

        # Limiter dans la plage [-127, 127]
        speed_g = max(min(int(speed_g), 125), -125)
        speed_d = max(min(int(speed_d), 125), -125)

        # Envoyer aux moteurs
        controller.set_raw_motor_speed(speed_g, speed_d)
        print(f"L={speed_g}  R={speed_d} err={error}  cmd=({speed_g},{speed_d})")
        
        time.sleep(0.1)

        # Récupération des ticks des encodeurs pour vérifier le déplacement
        left_ticks, right_ticks=controller.get_encoder_ticks()
        print(f"Ticks après le déplacement : gauche={left_ticks}, droite={right_ticks}")
        controller.new_relative()
        total_ticks += abs(left_ticks + right_ticks)/2
        print(f"Ticks total après le déplacement {total_ticks}")   
    
    print(f"distance réellement parcourue : {calcul_distance(total_ticks)}")
    print(f"distance demandée {calcul_distance(ticks_max)}")
    
    # Stop moteur
    controller.standby()