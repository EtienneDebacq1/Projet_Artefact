import requests as req

URL = "http://proj103.r2.enst.fr/api"


def post_pos(x=0, y=0, angle=0, id_groupe=0):
    """ Envoie de la position au serveur.

    Args:
        x (int, optional): Coordonnées x où le robot se trouve. Defaults to 0.
        y (int, optional): Coordonnées y où le robot se trouve. Defaults to 0.
        angle (int, optional): Angle par rapport à la balise en (1,5; 0). Defaults to 0.
        id_groupe (int, optional): Paramètre à mettre à 7 pour l'évaluation intermédiaire. Defaults to 0.
    """
    if id_groupe == 7:
        reponse = req.post(f"{URL}/pos?x={x}&y={y}&angle={angle}")
        print(f"Response from server: {reponse.status_code} - {reponse.text}")
        return reponse
    else:
        reponse = req.post(f"{URL}/pos?x={x}&y={y}&angle={angle}")
        print(f"Response from server: {reponse.status_code} - {reponse.text}")
        return reponse



def get_list():
    """ Récupère la liste des balises à capturer.

    Returns:
        int list : les id des balises à capturer. 
    """
    try :
        reponse = req.get(f"{URL}/list")
        reponse = reponse.json()
        return reponse["markers"][0]
    except Exception as e:
        print(f"Error fetching list: {e}")
        return 10

def post_list(id, sect, inner):
    """ Envoie de la capture d'un drapeau.

    Args:
        id (int): entier entre 5 et 16.
        sect (str): lettre entre A et H.
        inner (int): 1 pour le cercle intérieur et 0 pour le cercle extérieur.
    """
    reponse = req.post(f"{URL}/marker?id={id}&sector={sect}&inner={inner}")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")
    return reponse


def get_pos():
    """ Vérifie si le drapeau est validé.

    Returns:
        bool: rien si pas validé, false si en attente de validation et true si validé.
    """
    reponse = req.get(f"{URL}/status")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")
    if reponse.status_code == 401 or reponse.status_code == 400:
        return (0, 0, 0)
    positions = reponse.json()["positions"]
    position = [p for p in positions if p["team"] == 3]
    if not position:
        return (0, 0, 0)
    return (position["x"], position["y"], position["theta"])


def post_start():
    """ Commence la course. 
    """
    reponse = req.post(f"{URL}/start")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")
    return reponse


def post_stop():
    """ Termine la course.
    """
    reponse = req.post(f"{URL}/stop")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")
    return reponse

def post_pattern(N):
    """ Choisi le motif de course N. Ne peut pas être changé en pleine course.
    """
    reponse = req.post(f"{URL}/pattern?idx={N}")
    return reponse


def get_pattern():
    """ Récupère le motif de parcours choisi.

    Returns:
        liste de balises : celle choisie par le motif.
    """
    reponse = req.get(f"{URL}/pattern").json()[0]
    return reponse


def post_maj(rid, val, tid=0):
    """ Accède aux 5 registres tous de 1ko de mémoire.

    Args:
        rid (int): id de registre dans [|1; 5|] 
        val (bool): true = modification pour tous les robots du groupe et false = modification uniquement pour le demandeur
        tid (int): si tid est renseigné, modifie le registre pour le robot de l'équipe tid, sinon modifie uniquement celui du demandeur
    """
    if tid == 0:
        req.post(f"{URL}/udta?idx={rid}&all={val}")
    else:
        req.post(f"{URL}/udta?idx={rid}&all={val}&t={tid}")


def get_maj(rid, tid):
    """ Récupère les données des registres selon les arguments.

    Args:
        rid (int): identifiant du registre entre 1 et 5.
        tid (int): identifiant de l’équipe depuis laquelle lire le registre entre 1 et 5. Si le paramètre est absent, lecture de la mémoire du demandeur.
    """
    return req.get(f"{URL}/udta?idx={rid}&t={tid}").json()[0]