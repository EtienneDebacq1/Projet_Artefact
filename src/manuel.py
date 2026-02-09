import controller as controller
import time
import threading

c = controller.Controller()

c.set_motor_shutdown_timeout(0.5)

thread_loop = True
command = "0"  # commande par défaut : arrêt des moteurs

def avancer(direction):
    global command
    command = direction
    # Se connecter au contrôlleur (par défaut sur i2c-8)

    # Le contrôleur éteint les moteurs au bout de 4 secondes
    # s'il ne reçoit pas de commande
    # Le défaut est de 0.5s

    # Change la vitesse des moteurs (mode asservi/contrôlé PID)
    # - le signe de la vitesse changera le sens de rotation
    # - est exprimée en nombre d'impulsions des capteurs par 1/100s

    # Imprime l'incrément du compteur d'impulsions
    print(c.get_encoder_ticks())

    

# En mode non asservi on peut utiliser
# c.set_raw_motor_speed avec des vitesses entre -127 et +127
# pour changer le rapport cyclique des PWM des moteurs

# Pour arrêter les deux moteurs
# c.standby()

# Pour avoir la doc complète
# help(controller.Controller)

def moteur_loop():
    global command
    while thread_loop : 
        if command == "1":
            c.set_motor_speed(110, 110)
        elif command == "2":
            c.set_motor_speed(-100, -100)
        elif command == "3":
            c.set_motor_speed(-60, 60)
        elif command == "4":
            c.set_motor_speed(60, -60)
        else:
            # STOP
            c.set_motor_speed(0, 0)

        time.sleep(0.05)   # evite de bloquer le CPU

def stop_moteur_loop():
    global thread_loop
    thread_loop = False

# Lancer la boucle en arrière-plan AU DEMARRAGE
threading.Thread(target=moteur_loop, daemon=True).start()