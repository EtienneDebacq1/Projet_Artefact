"""Module for robot functionality."""
from cv2 import aruco
import controller
import cv2
import numpy as np

def setup_camera():
    """
    Configuration de la caméra pour la capture vidéo.
    """
    cap_setup = cv2.VideoCapture(0)
    cap_setup.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap_setup.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

    data = np.load('src/camera/calibration_params.npz')
    cameraMatrix_setup = data['cameraMatrix']
    distCoeffs_setup = data['distCoeffs']
    return cap_setup, cameraMatrix_setup, distCoeffs_setup

controller = controller.Controller()
controller.set_motor_shutdown_timeout(5)

aruco_dict_type=aruco.DICT_6X6_50
ARUCO_DICT = aruco.getPredefinedDictionary(aruco_dict_type)
parameters = aruco.DetectorParameters()
cap , cameraMatrix, distCoeffs = setup_camera()

detector = aruco.ArucoDetector(ARUCO_DICT, parameters)