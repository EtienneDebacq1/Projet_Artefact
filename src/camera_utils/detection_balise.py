import cv2
import cv2.aruco as aruco
from src.rasberry.balise import Balise
import numpy as np
import time
from src.rasberry.camera.take_pictures import save_last_frame

def setup_camera():
    """
    Configuration de la caméra pour la capture vidéo.
    """
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

    data = np.load('src/rasberry/camera/calibration_params.npz')
    cameraMatrix = data['cameraMatrix']
    distCoeffs = data['distCoeffs']
    return cap, cameraMatrix, distCoeffs

def detection_balise():
    """
    Test de détection des marqueurs ArUco dans une image.
    """
    cap, cameraMatrix, distCoeffs = setup_camera()
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    while(True):
        ret, frame = cap.read()

        if not ret:
            break

        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(frame)

        if corners :
            aruco.drawDetectedMarkers(frame, corners, ids)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def rvec_to_euler(rvec):
    # Convertit le vecteur de rotation en matrice 3x3
    R, _ = cv2.Rodrigues(rvec)

    sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])

    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(R[2,1], R[2,2])  
        y = np.arctan2(-R[2,0], sy)      
        z = np.arctan2(R[1,0], R[0,0])   
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0

    # Convertir en degrés
    return np.degrees([x, y, z])

def calculate_distance_n_fois(cap, cameraMatrix, distCoeffs, n=2, marker_size=0.02):
    cap.read()
    balises = send_distance(cap, cameraMatrix, distCoeffs, marker_size)
 
    return balises

def send_distance(cap, cameraMatrix, distCoeffs, marker_size=0.02):

    aruco_dict_type=aruco.DICT_6X6_50
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = aruco.DetectorParameters()

    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # 🔥 vider le buffer caméra AVANT la lecture
    for _ in range(3):
        cap.read()

    # 🔥 maintenant on lit la frame ACTUELLE
    ret, frame = cap.read()

    if not ret:
        print("Erreur : impossible de lire l'image depuis la caméra.")
        return None
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    save_last_frame(gray)

    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is None :
        return []
    
    half = marker_size / 2.0
    
    obj_points = np.array([
        [-half,  half, 0],
        [ half,  half, 0],
        [ half, -half, 0],
        [-half, -half, 0]
    ], dtype=np.float32)

    poses = []
    for i, marker_id in enumerate(ids.flatten()):
        _, rvec, tvec,  = cv2.solvePnP(
            obj_points, corners[i], cameraMatrix, distCoeffs
        )

        distance = float(np.linalg.norm(tvec)) * 100  # en cm
        x = tvec[0][0]  # position horizontale
        z = tvec[2][0]  # profondeur
        angle_h = np.degrees(np.arctan2(x, z))

        poses.append(Balise(marker_id, None, None, distance, angle_h))

    
    return poses
    
if __name__ == "__main__":
    cap , cameraMatrix, distCoeffs = setup_camera()
    while True:
        poses = send_distance(cap, cameraMatrix, distCoeffs)
        for pose in poses:
            marker_id, distance, rotx, roty, rotz = pose
            print(f"ID: {marker_id}, Distance: {distance:.2f} m, Rotation (X,Y,Z): ({rotx:.2f}, {roty:.2f}, {rotz:.2f})")


