# Résultat des tests pour le module mouvement.py



import time
from src.robot import controller
from src.mouvement import avancer

def determine_impulsions() :
    """Détermine le nombre d'impulsions pour 100 cm et 50 cm.
    [TEST RESULT] : 160 impulsions par cm.
    """
    controller.set_motor_speed(40, 40)
    initial_ticks = controller.get_encoder_ticks()
    # Avancer pendant 3 secondes
    time.sleep(3)
    controller.standby()
    time.sleep(1)
    final_ticks = controller.get_encoder_ticks()
    longueur_mesuree = input("Entrez la distance réelle parcourue en cm : ")
    diff_left = final_ticks[0] - initial_ticks[0]
    diff_right = final_ticks[1] - initial_ticks[1]
    avg_diff = (diff_left + diff_right) / 2

    impulsions_par_cm = avg_diff / int(longueur_mesuree)

    print(f"Ticks Gauche: {diff_left}, Ticks Droite: {diff_right}")
    print(f"Moyenne: {avg_diff}")
    print(f"Résultat final : {impulsions_par_cm} impulsions/cm")

def test_avancer(distance_cm: int):
    # Avancer le robot de 50 cm : réussite
    # Avancer le robot de 30 cm : réussite
    # Avancer le robot de 100 cm : réussite à 5 cm près
    """Test d'avancer le robot de distance_cm centimètres."""
    print(f"Test : Avancer de {distance_cm} cm")
    avancer(distance_cm)
    print("Test terminé.")

if __name__ == "__main__":
    choix = input("Voulez-vous déterminer les impulsions par cm ? (o/n) : ")
    if choix.lower() == 'o':
        determine_impulsions()
    else :
        longueur = int(input("Entrez la distance à avancer en cm : "))
        test_avancer(longueur)