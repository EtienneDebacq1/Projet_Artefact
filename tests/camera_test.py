from src.camera import detectAruco, calculate_distance_angle

def test_detect_markers(has_aruco):
    """
    Teste la détection des marqueurs ArUco dans une image donnée.
    [RESULTAT] = succeed
    """
    corners, ids, frame = detect_aruco()

    if has_aruco:
        id_detect = int(input("Entrez l'ID du marqueur attendu : "))
        assert ids is not None and len(ids) > 0, "Aucun marqueur ArUco détecté, mais des marqueurs étaient présents."
        assert id_detect in ids, f"Le marqueur ArUco avec l'ID {id_detect} n'a pas été détecté."
    else:
        assert ids is None or len(ids) == 0, "Des marqueurs ArUco ont été détectés, mais aucun marqueur n'était présent."

    print("Test de détection des marqueurs ArUco réussi.")
 
def test_calculate_distance_angle():
    """
    Teste le calcul de la distance et de l'angle aux marqueurs ArUco détectés.
    [RESULTAT] = succeed à 5 cm près pour la distance.
    """
    ids, corners = detectAruco()

    if ids is None or len(ids) == 0:
        print("Aucun marqueur ArUco détecté pour le test de distance et d'angle.")
        return

    poses = calculate_distance_angle(corners, ids, marker_size=0.10)

    for pose in poses:
        print(f"Marqueur ID: {pose.id}, Distance: {pose.dist:.2f} cm, Angle: {pose.angle:.2f} degrés")


if __name__ == "__main__":
    choix = input("Voulez-vous tester la détection des marqueurs ArUco (1) ou le calcul de distance et angle (2) ? ")
    if choix == '2':
        test_calculate_distance_angle()
    else:
        has_aruco_input = input("L'image contient-elle des marqueurs ArUco ? (o/n) : ").strip().lower()
        has_aruco = has_aruco_input == 'o'
        test_detect_markers(has_aruco)
