

from src.mouvement import danse
from controller import Controller


if __name__ == "__main__":
    controller = Controller()
    controller.set_motor_shutdown_timeout(5)
    danse(controller)