from src.mouvement import tourner_droite, tourner_gauche
from controller import Controller

# Résultat des tests pour la rotation du robot
# Sens droite : réussite
# Sens gauche : réussite


if __name__ == "__main__":
    controller = Controller()
    controller.set_motor_shutdown_timeout(5)
    sens = int(input("Entrez le sens de rotation (1 pour droite, -1 pour gauche) : "))
    if sens == 1:
        print("Test : Tourner à droite de 15 degrés")
        tourner_droite(controller)
    elif sens == -1:
        print("Test : Tourner à gauche de 15 degrés")
        tourner_gauche(controller)
    else:
        print("Sens invalide. Veuillez entrer 1 ou -1.")