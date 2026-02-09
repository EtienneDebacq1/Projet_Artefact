import sys
import os

# --- CORRECTION DU PATH ---
# On ajoute le dossier parent (team3) au chemin de recherche de Python
# pour qu'il puisse trouver le dossier 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --------------------------

from src.camera import detectAruco, calculate_distance_angle, init_balise, position

def test_position_robot():
    """
    Teste le calcul de la position absolue (X, Y) du robot sur le terrain.
    [RESULTAT] = Les coordonnées affichées doivent correspondre à la réalité.
    """
    print("\n--- Démarrage du test de position ---")
    
    # 1. Détection
    # Note: detectAruco utilise 'cap' qui est initialisé dans src/robot.py
    # Assure-toi que la caméra est bien accessible.
    try:
        res = detectAruco()
    except Exception as e:
        print(f"Erreur lors de l'accès caméra : {e}")
        return

    # Gestion du cas où detectAruco renverrait None
    if res is None:
        print("Erreur : Impossible de récupérer une image.")
        return
        
    ids, corners = res

    if ids is None or len(ids) == 0:
        print("ÉCHEC : Aucun marqueur ArUco détecté. Impossible de calculer la position.")
        return

    # 2. Calcul des distances/angles
    poses = calculate_distance_angle(corners, ids)

    print(f"{len(poses)} marqueur(s) détecté(s). Calcul de la position...\n")

    found_balise = False
    for aruco_obj in poses:
        # 3. Initialisation des coordonnées de la balise
        aruco_obj = init_balise(aruco_obj)

        # Si x est NaN, c'est que l'ID n'est pas 1, 2, 3 ou 4
        if aruco_obj.x != aruco_obj.x: 
             print(f"[ID {aruco_obj.id}] Ignoré : Ce n'est pas une balise de terrain connue.")
             continue
        
        found_balise = True

        # 4. Appel de la fonction à tester
        x_robot, y_robot = position(aruco_obj)

        # 5. Affichage des résultats
        print(f"--- Résultat pour Marqueur ID {aruco_obj.id} ---")
        print(f"  Données brutes : Dist={aruco_obj.dist:.1f}cm | Angle={aruco_obj.angle:.1f}°")
        print(f"  Position Balise: x={aruco_obj.x}, y={aruco_obj.y}")
        print(f"  >> POSITION ROBOT CALCULÉE : X = {x_robot:.2f}, Y = {y_robot:.2f}")
        print("---------------------------------------------")

    if not found_balise:
        print("Aucune balise officielle (ID 1 à 4) n'a été trouvée parmi les marqueurs.")

if __name__ == "__main__":
    print("Placez le robot face à une balise (ID 1, 2, 3 ou 4).")
    input("Appuyez sur Entrée pour lancer la détection...")
    test_position_robot()