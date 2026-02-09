import numpy as np
import cv2 as cv
from cv2 import aruco
import glob

def detect_markers(img):
    """
    Test de détection des marqueurs ArUco dans une image.
    """
    
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector = aruco.ArucoDetector(aruco_dict, aruco.DetectorParameters())

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    print("IDs détectés :", ids)

    frame = aruco.drawDetectedMarkers(img.copy(), corners, ids)
    cv.imshow("Detection test", frame)
    cv.waitKey(0)

def has_sufficient_markers(img, threshold=8):
    """ 
    Vérifie si une image contient au moins `threshold` marqueurs ArUco détectés.
    """
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector = aruco.ArucoDetector(aruco_dict, aruco.DetectorParameters())

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    n_markers = 0 if ids is None else len(ids)
    print(f"Nombre de marqueurs détectés: {n_markers}")
    return n_markers >= threshold

def keep_great_image(images):
    """
    Filtre les images pour ne garder que celles avec suffisamment de marqueurs ArUco détectés.
    """
    
    good_images = []
    for img in images:
        if has_sufficient_markers(img):
            good_images.append(img)
    return good_images

def calibrate_camera(calibration_images):
    """
    Calibre la caméra en utilisant les images de calibration fournies.
    """
    
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    board = aruco.CharucoBoard(
        size=(7, 7),          # nb de cases
        squareLength=0.015,   # 15 mm = 0.015 m
        markerLength=0.011,   # 11 mm = 0.011 m
        dictionary=aruco_dict
    )

    charuco_corners = []
    charuco_ids = []
    detector_charuco = cv.aruco.CharucoDetector(board)
    
    image_size = None

    for img in calibration_images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        res = detector_charuco.detectBoard(gray)
        
        print(img.shape)

        if isinstance(res, tuple):
            corners, ids = res[0], res[1]
        else:
            corners, ids = getattr(res, "charucoCorners", None), getattr(res, "charucoIds", None)

        n = 0 if corners is None else len(corners)
        print(f"Image calibration: detected {n} Charuco corners")

        if ids is not None and n > 8:
            charuco_corners.append(corners)
            charuco_ids.append(ids)


        if image_size is None:
            image_size = img.shape[1], img.shape[0]

    print(f"Coins Charuco: {len(charuco_corners)}")

    obj_points = []
    img_points = []

    for corners, ids in zip(charuco_corners, charuco_ids):
        if corners is None or ids is None or len(ids) < 4:
            continue  # on saute les images insuffisantes

        obj_pts = board.getChessboardCorners()[ids.flatten(), :]
        obj_points.append(obj_pts.astype(np.float32))
        img_points.append(corners.reshape(-1, 2).astype(np.float32))

    ret, K, D, _, _ = cv.calibrateCamera(
        obj_points, img_points, image_size, None, None
    )
    print("Calibration RMS error:", ret)
    print("Camera matrix:\n", K)
    print("Distortion coefficients:\n", D) 

    with open('src/rasberry/camera/calibration_params.npz', 'wb') as f:
       np.savez(f, cameraMatrix=K, distCoeffs=D)



if __name__ == "__main__":
    calibration_images = [cv.imread(file) for file in glob.glob('src/rasberry/camera/calibration_images/*.jpg')]
    print("Starting camera calibration...")
    print(f"Number of calibration images: {len(calibration_images)}")
    good_images = keep_great_image(calibration_images)
    print(f"Number of good calibration images: {len(good_images)}")

    calibrate_camera(good_images)