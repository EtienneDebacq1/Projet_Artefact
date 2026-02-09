import cv2
import os

def save_last_frame(frame, path="static/frame.jpg"):
    os.makedirs("static", exist_ok=True)
    cv2.imwrite(path, frame)

def take_pictures():
    
    import time
    cam = cv2.VideoCapture(0)
    for i in range(150):
        time.sleep(0.2)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(f'src/rasberry/camera/calibration_images/image_{i}.jpg', frame)
            print(f'Captured image_{i}.jpg')
      
        cv2.imshow('Captured Image', frame)
        cv2.waitKey(1)  
    cam.release()
    cv2.destroyAllWindows()

def take_one_picture():
    import cv2
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite('src/rasberry/camera/images/picture.jpg', frame)
        print('Captured picture.jpg')
    cam.release()

if __name__ == "__main__":
    take_pictures()