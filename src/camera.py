"""Module for camera functionality."""
import cv2
import math
import numpy as np
import os
from src.robot import detector, cap, cameraMatrix, distCoeffs

SIZE_DRAPEAU = 0.10
SIZE_BALISE = 0.02

class aruco_c:
    def __init__ (self, id, corners, dist=math.nan, angle=math.nan, x=math.nan, y=math.nan):
        self.id = id                #Id de l'aruco
        self.corners = corners      #Coins de l'aruco dans l'ordre suivant : haut gauche, haut droit, bas droit et bas gauche
        print("id dans aruco_c :", id)
        self.size = SIZE_BALISE if (id > 4 or id == 0) else SIZE_DRAPEAU
        self.dist = dist        #Distance de aruco (initialisé a infini)
        self.angle = angle       #l'angle en question
        self.x = x          #Position réelle de l'acuro en x
        self.y = y          #Position réelle de l'acuro en y


def save_last_frame(frame, path="static/frame.jpg"):
    os.makedirs("static", exist_ok=True)
    cv2.imwrite(path, frame)

def detectAruco():
    """Detect ArUco markers in the current frame from the camera."""
    ret, frame = cap.read()

    if not ret:
        print("Erreur : impossible de lire l'image depuis la caméra.")
        return None
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    save_last_frame(gray)

    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is None:
        ids = []
        corners = []
    else :
        ids = ids[0]
        corners = corners[0]
    
    return ids, corners

def calculate_distance_angle(corners, ids : np.ndarray, marker_size=0.1) -> list[aruco_c]:
    """Calculate the distance to detected ArUco markers."""
    if ids is None:
        return []
    
    print("size drapeau dans calc :", marker_size)

    half = marker_size / 2.0
    
    obj_points = np.array([
        [-half,  half, 0],
        [ half,  half, 0],
        [ half, -half, 0],
        [-half, -half, 0]
    ], dtype=np.float32)

    poses = []
    ids = np.array(ids)

    for i, marker_id in enumerate(ids.flatten()):
        c = np.asarray(corners[i], dtype=np.float32)

        if c.ndim == 3:
            c = c.reshape(-1, 2)
        elif c.ndim == 2:
            pass
        else:
            raise ValueError(f"Forme inattendue pour corners[{i}] : {c.shape}")

        if c.shape[0] < 4:
            raise ValueError(
                f"Pas assez de points image pour solvePnP : {c.shape[0]} (attendu >= 4)"
            )

        image_points = c[:4, :] 

        retval, rvec, tvec = cv2.solvePnP(
            obj_points, image_points, cameraMatrix, distCoeffs
        )

        distance = float(np.linalg.norm(tvec)) * 100  # cm

        hg = corners[i][0] #Coin en haut a gauche
        hd = corners[i][1] #Coin en haut a droite
        bd = corners[i][2] #Coin en bas a droite
        bg = corners[i][3] #Coin en bas a gauche

        #Calcul de la distance

        #Définition des valeurs
        taille_px_gauche = np.sqrt((hg[0] - bg[0])**2 + (hg[1] - bg[1])**2)
        taille_px_droit = np.sqrt((hd[0] - bd[0])**2 + (hd[1] - bd[1])**2)
        taille_px_mid = (taille_px_droit + taille_px_gauche)/2 #Moyenne de la longueur du coté gauche et du coté droit
        taille_px_bas = np.sqrt((bd[0] - bg[0])**2 + (bd[1] - bg[1])**2)
        taille_px_haut = np.sqrt((hd[0] - hg[0])**2 + (hd[1] - hg[1])**2)
        moy_horiz = (taille_px_bas + taille_px_haut)/2
        echelle = marker_size / taille_px_mid

        #Calcul de l'angle
        taille_horiz_norm = moy_horiz * echelle/marker_size
        angle = 0
        if taille_horiz_norm < 1:
            va_angle = np.arccos(taille_horiz_norm)
            if taille_px_gauche > taille_px_droit:
                angle = -va_angle
            else:
                angle = va_angle

        print(f"angle = {math.degrees(angle):.1f}°")

        poses.append(
            aruco_c(int(marker_id), corners[i], dist = distance , angle=angle)
        )

    return poses

def camera_open():
    if not cap.isOpened():
        cap.open(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("Camera ouverte.")

def camera_close():
    if cap.isOpened():
        cap.release()
    print("Camera fermée.")

def recupere_photo():
    if not cap.isOpened():
        print("Erreur: Caméra fermée")
        return None

    # Premier grab pour vider le buffer
    cap.grab()
    
    # Deuxième grab qu'on garde
    ret, frame = cap.read()

    if ret:
        save_last_frame(frame)
        return frame
    else:
        print("Erreur de lecture frame")
        return None
    
def init_balise(aruco):
    id_balise = aruco.id
    aruco.size = SIZE_DRAPEAU

    if id_balise == 1:
        aruco.x = 0
        aruco.y = 150
    elif id_balise == 2:
        aruco.x = 150
        aruco.y = 0
    elif id_balise == 3:
        aruco.x = 0
        aruco.y = -150
    elif id_balise == 4:
        aruco.x = -150
        aruco.y = 0


    return aruco


def distance_aruco(aruco_obj : aruco_c) -> float :

    balise = calculate_distance_angle([aruco_obj.corners], np.array([aruco_obj.id]), aruco_obj.size)[0]
    
    aruco_obj.dist = balise.dist
    return aruco_obj.dist


def angle_aruco(aruco_obj : aruco_c) -> float:

    balise = calculate_distance_angle([aruco_obj.corners], np.array([aruco_obj.id]), aruco_obj.size)[0]
    
    return balise.angle

def position(aruco_obj : aruco_c) -> tuple[float, float] :
    angle = angle_aruco(aruco_obj)
    id = aruco_obj.id
    alpha = math.atan((aruco_obj.dist * math.sin(angle))/(150 - aruco_obj.dist * math.cos(angle)) )
    if id == 1:
        x_robot = aruco_obj.x + aruco_obj.dist * math.sin(angle)
        y_robot = aruco_obj.y - aruco_obj.dist * math.cos(angle)  
        angle_reel = alpha

    if id == 2:
        x_robot = aruco_obj.x - aruco_obj.dist * math.cos(angle)
        y_robot = aruco_obj.y - aruco_obj.dist * math.sin(angle)
        angle_reel = math.pi/2 - alpha

    if id == 3:
        x_robot = aruco_obj.x - aruco_obj.dist * math.sin(angle)
        y_robot = aruco_obj.y + aruco_obj.dist * math.cos(angle)
        angle_reel = math.pi - alpha

    if id == 4:
        x_robot = aruco_obj.x + aruco_obj.dist * math.cos(angle)
        y_robot = aruco_obj.y + aruco_obj.dist * math.sin(angle)
        angle_reel = 3*math.pi/2 - alpha

        
    
    return (x_robot, y_robot, angle_reel)