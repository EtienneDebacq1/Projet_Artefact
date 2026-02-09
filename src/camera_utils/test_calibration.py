import cv2 as cv
import numpy as np

def test_undistortion():
    # Calibration params
    data = np.load('src/rasberry/camera/calibration_params.npz')
    cameraMatrix = data['cameraMatrix']
    distCoeffs = data['distCoeffs']

    # Test image
    img = cv.imread('src/rasberry/camera/images/test_image.jpg')
    h, w = img.shape[:2]

    # Undistort
    newK, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w, h), 1, (w, h))
    undistorted = cv.undistort(img, cameraMatrix, distCoeffs, None, newK)

    # Show side by side
    combined = cv.hconcat([img, undistorted])
    cv.imshow("Gauche = originale | Droite = corrigée", combined)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    test_undistortion()