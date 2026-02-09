from controller import *
import src.mouvement as mouvement
import src.camera as camera

class robot:
    def __init__(self, i2c_bus=8):
        self.ctrl = Controller(i2c_bus)
        self.ctrl.set_motor_shutdown_timeout(5)
    
    def arret(self):
        self.ctrl.standby()
   
    def tourner_gauche(self):
        mouvement.tourner_gauche(self.ctrl)

    def tourner_droite(self):
        mouvement.tourner_droite(self.ctrl)
    
    
    def avancer(self, distance):
        mouvement.avancer(self.ctrl, distance)
    
    def reculer(self, distance):
        mouvement.arriere(self.ctrl, distance)
        
    def danse(self, sens):
        mouvement.danse(self.ctrl, sens)

    def camera_open(self):
        camera.camera_open()

    def camera_close(self):
        camera.camera_close()

    def recupere_photo(self):
        return camera.recupere_photo()

    def distance_aruco(self, aruco_obj):
        return camera.distance_aruco(aruco_obj)

    def angle_aruco(self, aruco_obj):
        return camera.angle_aruco(aruco_obj)

    def init_balise(self, aruco):
        return camera.init_balise(aruco)

 

if __name__ == '__main__':
    print("py file launched directly")
    print("testing motor")
    robot_py = robot(i2c_bus=8)