
import cv2
import os
from src.robot import cap

def take_photo(path="static/frame.jpg"):
    """Capture une photo depuis la caméra et la sauvegarde."""

    ret, frame = cap.read()

    if not ret:
        print("Erreur : impossible de lire l'image depuis la caméra.")
        return None

    os.makedirs("static", exist_ok=True)
    print("Saving photo to", path)
    cv2.imwrite(path, frame)
    return frame

if __name__ == "__main__":
    take_photo()