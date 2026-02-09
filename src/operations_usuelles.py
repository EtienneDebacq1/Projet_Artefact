import time
import math
import json
import numpy as np
import src.server_commun as serv
import src.camera as cam
import src.rob as rob
import requests as req
import threading

sect = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
nb_tour_complet = 36 #Nb de "tourner" pour faire un tour complet (si possible divisible par 4) ?team?
safety_dist = 15 #en cm ?team?
URL = "http://proj103.r2.enst.fr/api"
secteur_de_depart = 4

class robot_c:
    def __init__ (self):
        #Dernière position trouvée a partir d'une balise
        self.xb = math.nan 
        self.yb = math.nan
        self.angleb = math.nan
        #Position estimée du robot (basé sur ses déplacements depuis la dernière position théorique)
        #Initialisation arbitraire, seront modifié selon les robots
        self.xa = 180
        self.ya = 0
        self.anglea = np.pi
    
    def posR(self,x,y): #Update la position du robot après la vue d'une balise
        self.xb = x
        self.yb = y
        self.xa = x
        self.ya = y
    
    def posA(self,x,y): #Update la position du robot après un déplacement
        self.xa = x
        self.ya = y
    
    def getPosR(self):
        return self.xb,self.yb

    def getPosA(self):
        return self.xa,self.ya

robot = robot_c()
r_pi = rob.robot()
dico = {}
id_robot = 3 

#Fonction qui gère la vue d'une balise
def updateBalise(id : int, corners):
    if (id not in dico.keys()):
        dico[id] = cam.aruco_c(id,corners) #Crée l'object dans le dictionnaire
        dico[id].dist = cam.distance_aruco(dico[id]) #Calcule la distance du robot à l'aruco
        print("distance :", dico[id].dist)
        dico[id] = cam.init_balise(dico[id]) #Initialise la balise avec ses coordonnées
        return cam.position(dico[id]) #Calcul et renvoie la position du robot par rapport à la balise
    else:
        dico[id].corners = corners
        dico[id].dist = cam.distance_aruco(dico[id]) #Calcule la distance du robot à l'aruco
        print("distance :", dico[id].dist)
        return cam.position(dico[id]) #Calcul et renvoie la position du robot par rapport à la balise

def updateDrapeau(id : int, corners):
    if (id not in dico.keys()):
        dico[id] = cam.aruco_c(id,corners)
        dico[id].dist = cam.distance_aruco(dico[id])
        dico[id].angle = cam.angle_aruco(dico[id])
        return (dico[id].dist,dico[id].angle)
    else:
        dico[id].corners = corners
        dico[id].dist = cam.distance_aruco(dico[id])
        dico[id].angle = cam.angle_aruco(dico[id])
        return (dico[id].dist,dico[id].angle)

def tourner(i):
    if i > 0:
        r_pi.tourner_droite()
        robot.anglea -= 15*np.pi/180 #?team?
    else:
        r_pi.tourner_gauche() 
        robot.anglea += 15*np.pi/180 #?team?

# TODO : faire une fonction avancer_cm qui en plus, update la position x et y du robot

def getPrecisePos(sens): #Sens est soit 1 soit -1 selon le sens (ie commence à tourner à gauche si -1 et commence à droite si -1)
    nbBaliseVu = 0
    pRobot = []
    cpt = 0

    #Récupération des deux photos
    cam.recupere_photo()

    #Détection des aruco
    ids, corners = cam.detectAruco()
    time.sleep(0.2)
    while (nbBaliseVu < 2):
        for ident in ids:
            if (0 < ident and 5 > ident): #Regarde si l'aruco est une balise 
                k = np.where(ids == ident)[0][0] #Gestion de la position
                pRobot.append(updateBalise(int(ids[k]), corners[k])) #Position en x et y du robot par rapport à la balise 1
                nbBaliseVu = nbBaliseVu + 1
        tourner(sens)
        cpt = cpt + 1
        time.sleep(0.2)

        #Récupération des deux photos
        cam.recupere_photo()

        #Détection des aruco
        ids, corners = cam.detectAruco()

    for i in range(cpt): #Reviens à sa position intiale (Qst ?)
        tourner(-sens)
        time.sleep(0.2)
    
    return ((pRobot[0][0] + pRobot[1][0])/2, (pRobot[0][1] + pRobot[1][1])/2) #Renvoie la position du robot


def viserBalise(id_balise, demi_tour=False):
    sens = 1 #(Qst ?), a determiner selon le sens de rotation des robots

    if demi_tour:
        for i in range(nb_tour_complet//2):
            tourner(sens)
            time.sleep(0.2)
    #Récupération des deux photos
    cam.recupere_photo()

    #Détection des aruco
    ids, corners = cam.detectAruco()
    time.sleep(0.2)

    nb_tour = 0
    nb_angle = 0

    while (id_balise not in ids):
        tourner(sens)
        time.sleep(0.2)

        #Récupération des deux photos
        cam.recupere_photo()

        #Détection des aruco
        ids, corners = cam.detectAruco()
        time.sleep(0.2)

        nb_angle = nb_angle + 1

        if nb_angle >= (nb_tour_complet):
            nb_tour = nb_tour + 1
            nb_angle = 0

        if nb_tour >= 2:
            avancer_update(20) #Avance de 20 cm si pas de balise vue après deux tours complets
            viserBalise(id_balise, True)
            return
    
    k = np.where(ids == id_balise)[0][0]
    pRobot = updateBalise(int(ids[k]), corners[k])
    robot.posR(pRobot[0], pRobot[1])
    robot.anglea = pRobot[2]

    return dico[id_balise].dist

def searchDrapeau(id_drapeaux, secteur):
    sens = 1 #(Qst ?), a determiner selon le sens de rotation des robots
    print(id_drapeaux)
    ids_vu = []
    detected_aruco = -1
    for i in range(nb_tour_complet//4-1): #Tourne de 90°
        tourner(sens)
        time.sleep(0.2)
    cam.recupere_photo()
    ids, corners = cam.detectAruco()
    for ident in ids:
        if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
            ids_vu.append(ident)
            (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
            if abs(angle) < ((20/360)*2*np.pi):
                avancer_update(dist-safety_dist)
                detected_aruco = ident
                r_pi.danse(1)
                r_pi.danse(-1)
                serv.capture_drapeau(ident, sect[secteur], 0)
                r_pi.reculer(dist-safety_dist)
    time.sleep(0.2)

    for i in range(2):

        tourner(sens)
        time.sleep(0.2)

        cam.recupere_photo()
        ids, corners = cam.detectAruco()
        for ident in ids:

            print(ident)
            if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
                ids_vu.append(ident)
                (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
                if abs(angle) < ((25/360)*2*np.pi):
                    avancer_update(dist-safety_dist)
                    detected_aruco = ident
                    r_pi.danse(1)
                    r_pi.danse(-1)
                    serv.capture_drapeau(ident, sect[secteur], 0)
                    r_pi.reculer(dist-safety_dist)
        time.sleep(0.2)
    print("a ba non")
    for i in range(2):
        tourner(-sens)
        time.sleep(0.2)
    print("ici 8")
    for i in range(2):
        tourner(-sens)
        time.sleep(0.2)
        cam.recupere_photo()
        ids, corners = cam.detectAruco()
        for ident in ids:
            if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
                ids_vu.append(ident)
                (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
                print("\n\n" + str(ident) + " : " + str(angle) + "\n\n")
                if abs(angle) < ((25/360)*2*np.pi):
                    avancer_update(dist-safety_dist)
                    detected_aruco = ident
                    r_pi.danse(1)
                    r_pi.danse(-1)
                    serv.capture_drapeau(ident, sect[secteur], 0)
                    r_pi.reculer(dist-safety_dist)
        time.sleep(0.2)

    for i in range(nb_tour_complet//4 - 3): #Tourne de 90°
        tourner(-sens)
        time.sleep(0.2)

    sens = -sens

    for i in range(nb_tour_complet//4-1): #Tourne de 90°
        tourner(sens)
        time.sleep(0.2)
    cam.recupere_photo()
    ids, corners = cam.detectAruco()
    for ident in ids:
        if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
            ids_vu.append(ident)
            (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
            print("\n\n" + str(ident) + " : " + str(angle) + "\n\n")
            if abs(angle) < ((25/360)*2*np.pi):
                avancer_update(dist-safety_dist)
                detected_aruco = ident
                r_pi.danse(1)
                r_pi.danse(-1)
                serv.capture_drapeau(ident, sect[secteur], 1)
                r_pi.reculer(dist-safety_dist)
    time.sleep(0.2)
    for i in range(2):
        tourner(sens)
        time.sleep(0.2)
        cam.recupere_photo()
        ids, corners = cam.detectAruco()
        for ident in ids:
            if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
                ids_vu.append(ident)
                (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
                print("\n\n" + str(ident) + " : " + str(angle) + "\n\n")
                if abs(angle) < ((25/360)*2*np.pi):
                    avancer_update(dist-safety_dist)
                    detected_aruco = ident
                    r_pi.danse(1)
                    r_pi.danse(-1)
                    serv.capture_drapeau(ident, sect[secteur], 1)
                    r_pi.reculer(dist-safety_dist)
        time.sleep(0.2)
    
    for i in range(2):
        tourner(-sens)
        time.sleep(0.2)
    for i in range(2):
        tourner(-sens)
        time.sleep(0.2)
        cam.recupere_photo()
        ids, corners = cam.detectAruco()
        for ident in ids:
            if (ident > 4) and (ident in id_drapeaux) and (detected_aruco == -1):
                ids_vu.append(ident)
                (dist, angle) = updateDrapeau(int(ident), corners[np.where(ids == ident)[0][0]])
                print("\n\n" + str(ident) + " : " + str(angle) + "\n\n")
                if abs(angle) < ((25/360)*2*np.pi):
                    avancer_update(dist-safety_dist)
                    detected_aruco = ident
                    r_pi.danse(1)
                    r_pi.danse(-1)
                    serv.capture_drapeau(ident, sect[secteur], 1)
                    r_pi.reculer(dist-safety_dist)
        time.sleep(0.2)
    print(ids_vu)
    return detected_aruco
    

#On stockera les secteurs sous la forme de fichier json de ce format : {"used_sector":[1,2], "flag_catched_1": false, "flag_catched_2": false}
def mouvPhase2(secteur, id_drapeaux, vague, attrap):
    #Prototypage de la fonction
    #
    zones_indisp = [0,1,2,3,4,5,6,7]
    new_secteur = (secteur + 1)%8
    new_id_drapeaux = id_drapeaux
    #1) On actualise toute les secondes le stockage des infos du serv global jusqu'à ce que le secteur "(secteur + 1)%8" soit libre
    while new_secteur in zones_indisp:
        zones_indisp = []
        time.sleep(0.2)
        for i in range(5):
            temp = serv.lecture(i+1)
            if temp == "":
                continue
            temp = json.loads(temp)

            for j in temp["used_sector"]:
                if not (j in zones_indisp):
                    zones_indisp.append(j)
            for j in temp["flag_catched_wave"]:
                if j in new_id_drapeaux:
                    new_id_drapeaux.remove(j)
        print(zones_indisp)

    print("phase 1 terminée")

    #2) Rendre indisponible le secteur visé
    try :
        old_registre = json.loads(serv.lecture(id_robot))
        old_registre["used_sector"].append(new_secteur)
        new_text = json.dumps(old_registre)
        serv.ecriture(id_robot, new_text, True)
    except :
        old_registre = {
            "used_sector": [new_secteur],
            "flag_catched_1": False,
            "flag_catched_2": False,
            "flag_catched_wave": []
        }


    print("secteur réservé")

    #3) Disjonction de cas selon la position sur les secteurs pour viser la bonne balise
    if (secteur % 2 != 0): #On est bientot arrivé à une balise
        viserBalise((7-secteur)//2 + 1)
        avancer_update(dico[(7-secteur)//2 + 1].dist - safety_dist)
        viserBalise((7-new_secteur)//2 + 1, True)

        print("balise visée")
            
        #4) Selon le secteur (un modulo 2), avancer de 1/4 de la distance par rapport à la balise, ou de 2/3
        avancer_update(dico[(7-new_secteur)//2 + 1].dist/3) # (Qst ?) un peu plus loin ?
    else:
        viserBalise((7-new_secteur)//2 + 1)

        #4) Selon le secteur (un modulo 2), avancer de 1/4 de la distance par rapport à la balise, ou de 2/3
        avancer_update(dico[(7-new_secteur)//2 + 1].dist/2) #(Qst ?) un peu plus loin

    print("avancé dans le secteur")

    #5) Libérer le secteur précédent
    try :
        old_registre = json.loads(serv.lecture(id_robot))
        old_registre["used_sector"].remove(secteur)
        new_text = json.dumps(old_registre)
        serv.ecriture(id_robot, new_text, True)
    except :
        old_registre = {
            "used_sector": [],
            "flag_catched_1": False,
            "flag_catched_2": False,
            "flag_catched_wave": []
        }
        print("Erreur lors de la libération du secteur précédent")

    print("secteur libéré")

    #6) Appeler une fonction qui cherche s'il voit la balise (tour sur lui même, potentielle avancée vers le centre du cercle si trop loin)
    drapeauDetected = searchDrapeau(new_id_drapeaux, new_secteur)
    print("drapeau cherché")

    if drapeauDetected != -1: #7) Si balise detectée, le marquer dans le serveur commun et appeler appeler mouvPhase2wait
        print("drapeau détecté")
        try :
            old_registre = json.loads(serv.lecture(id_robot))
            old_registre["flag_catched_" + str(vague)] = True
            old_registre["flag_catched_wave"] = [int(drapeauDetected)]
            print(old_registre)
            new_text = json.dumps(old_registre)
            serv.ecriture(id_robot, new_text, True)
        except :
            print("Erreur lors de la mise à jour du drapeau capturé")
        if attrap >= 1:
            return mouvPhase2wait(new_secteur, vague)
        else:
            return mouvPhase2(new_secteur, new_id_drapeaux, vague, attrap + 1) 
    else: #8) Si balise non detectée, rappeler récursivement mouvPhase2 avec même vague, meme id_drapeau et secteur = (secteur + 1)%8
        print("on continue")
        print(new_id_drapeaux)
        print(new_secteur)
        print(vague)
        return mouvPhase2(new_secteur, new_id_drapeaux, vague, attrap)

def mouvPhase2wait(secteur, vague):
    #Prototypage de la fonction
    #
    zones_indisp = [0,1,2,3,4,5,6,7]
    new_secteur = (secteur + 1)%8
    #1) On actualise toute les secondes le stockage des infos du serv global jusqu'à ce que le secteur "(secteur + 1)%8" soit libre
    while new_secteur in zones_indisp:
        zones_indisp = []
        time.sleep(0.2)
        for i in range(5):
            temp = serv.lecture(i+1)
            if temp == "":
                continue
            temp = json.loads(temp)

            for j in temp["used_sector"]:
                if not (j in zones_indisp):
                    zones_indisp.append(j)

    #2) Rendre indisponible le secteur visé
    try :
        old_registre = json.loads(serv.lecture(id_robot))
        old_registre["used_sector"].append(new_secteur)
        new_text = json.dumps(old_registre)
        serv.ecriture(id_robot, new_text, True)
    except :
        old_registre = {
            "used_sector": [new_secteur],
            "flag_catched_1": False,
            "flag_catched_2": False,
            "flag_catched_wave": []
        }
        print("Erreur lors de la réservation du secteur visé")

    #3) Disjonction de cas selon la position sur les secteurs pour viser la bonne balise
    if (secteur % 2 == 0): #On est bientot arrivé à une balise
        viserBalise((7-secteur)//2 + 1)
        avancer_update(dico[(7-secteur)//2 + 1].dist - safety_dist)
        viserBalise((7-new_secteur)//2 + 1, True)
            
        #4) Selon le secteur (un modulo 2), avancer de 1/4 de la distance par rapport à la balise, ou de 2/3
        avancer_update(dico[(7-new_secteur)//2 + 1].dist/4) #(Qst ?) Un peu plus loin ?
    else:
        viserBalise((7-new_secteur)//2 + 1)

        #4) Selon le secteur (un modulo 2), avancer de 1/4 de la distance par rapport à la balise, ou de 2/3
        avancer_update(dico[(7-new_secteur)//2 + 1].dist/2) #(Qst ?) Un peu plus loin ?
        
    #5) Libérer le secteur précédent#5) Libérer le secteur précédent
    print(serv.lecture(id_robot))
    try :
        old_registre = json.loads(serv.lecture(id_robot))
        old_registre["used_sector"].remove(secteur)
        new_text = json.dumps(old_registre)
        serv.ecriture(id_robot, new_text, True)
    except :
        old_registre = {
            "used_sector": [],
            "flag_catched_1": False,
            "flag_catched_2": False,
            "flag_catched_wave": []
        }
        print("Erreur lors de la libération du secteur précédent")
    #6) Si pas toute les balises de la vague ont été detectée et validée, se rappeler récursivement avec secteur = (secteur + 1)%8
    vague_complete = True
    for i in range(5):
        temp = json.loads(serv.lecture(i+1))
        categorie = "flag_catched_" + str(vague)
        vague_complete = vague_complete and temp[categorie]
    if not(vague_complete):
        return mouvPhase2wait(new_secteur, vague)
    else:
        return secteur

def avancer_update(distance):
    r_pi.avancer(distance)
    x_new = robot.xa + distance * np.cos(robot.anglea)
    y_new = robot.ya + distance * np.sin(robot.anglea)
    robot.posA(x_new, y_new)

def start_autonome(sector):
    """ Lance le mode autonome du robot pour la phase finale.
    """
    
    #Commentaire Grégoire : J'ai légèrement réorganisé pour pouvoir ajouter le cas du 5ème robot
    for i in range(5):
        serv.ecriture(i+1, "", True)
    cam.camera_open()
    avancer_update(100) # TODO : Voir jusqu'où on avance

    #position : tuple[int, int] = getPrecisePos(1) # TODO : Verifier s'il n'y a pas de prob pour chaque robot
    #print("position : " + str(position))
    #robot.posR(position[0], position[1])

    #sector = get_sector_from_position(robot.getPosR()) # TODO : Ecrite par luc 
    #print("secteur : " + str(sector)) 
    if (sector % 2 == 1): #Un seul robot normalement, ce robot aura besoin d'une manoeuvre
        balise_to_see = 4
        if (sector != 7):
            balise_to_see = (7-sector)//2
        viserBalise(balise_to_see) #Se calibre avec la balise suivante
        for i in range(nb_tour_complet//4):
            tourner(1)
            time.sleep(0.2)
        r_pi.reculer(50) # TODO : Voir jusqu'où on recule
    
    markers = serv.get_list() #TODO : vérifier le format, qu'il s'agit bien d'une liste

    # Partie suivante sert uniquement si on veut tester un robot individuellement sans faire crash, sinon, utiliser le code plus loin
    #Attention, il faut forcement passer par un dictionnaire qu'on converti en Json, sinon, ça merde
    """
    for i in range(5):
        serv.ecriture(i+1, '{"used_sector":[' + str(sector) + '],"flag_catched_1": false, "flag_catched_2": false}', True)
    """
    init_serveur = {"used_sector":[sector], "flag_catched_1": False, "flag_catched_2": False, "flag_catched_wave": []}
    serv.ecriture(id_robot, json.dumps(init_serveur), True)

    everyone_ready = False
    while not (everyone_ready):
        everyone_ready = True
        
        for i in range(5):
            if (serv.lecture(i+1) == ""):
                everyone_ready = False
                serv.ecriture(id_robot, json.dumps(init_serveur), True)
        time.sleep(1)
    serv.ecriture(id_robot, json.dumps(init_serveur), True)
    end_sector = mouvPhase2(sector, markers, 1, 0) 
    time.sleep(10) #Pour laisser le temps aux examinateurs de valider 
    markers = serv.get_list()
    end_sector = mouvPhase2(end_sector, markers, 2, 0)

    cam.camera_close()

def send_pos():
    while True:
        serv.post_pos(int(robot.getPosA()[0]), int(robot.getPosA()[1]), int(robot.anglea*180/np.pi), id_robot)
        time.sleep(1)

#serv.demarrer_course()
def start():
    threading.Thread(target=send_pos, daemon=True).start()
    start_autonome(secteur_de_depart)
    #cam.camera_open()
    #serv.ecriture(id_robot, '{"used_sector":[7], "flag_catched_1": false, "flag_catched_2": false, "flag_catched_wave": []}', True)
    #mouvPhase2(7,[9,7,5],1)
    #cam.camera_close()

#serv.arreter_course()


### UTILS (A REPLACER DANS UN AUTRE FICHIER ?) ###

def get_list() -> list[int]:
    """ Récupère la liste des balises à capturer.

    Returns:
        int list : les id des balises à capturer. 
    """
    try :
        reponse = req.get(f"{URL}/list")
        if reponse.status_code != 200:
            raise RuntimeError("Failed to get list from server")
        reponse = reponse.json()
        return reponse["markers"]
    except Exception as e:
        print(f"Error fetching list: {e}")
        return []
    
def get_sector_from_position(position : tuple[int, int]) -> int:
    """ Détermine le secteur dans lequel se trouve le robot en fonction de sa position.

    Args:
        position (tuple[int, int]): La position (x, y) du robot.

    Returns:
        int: Le secteur dans lequel se trouve le robot (0 à 7).
    """
    x, y = position
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    sector = int((angle / (2 * math.pi)) * 8) % 8
    return sector

if __name__ == "__main__":
    start()