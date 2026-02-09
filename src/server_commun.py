
import requests as req

BASE_URL = "http://proj103.r2.enst.fr/api"
TIMEOUT = 5  # seconds

def _check_response(resp):
    resp.raise_for_status()


## Ecriture dans un registre
def ecriture(idx, data, all=False, team=None):
    """
    idx : registre [1..5]
    data : str (UTF-8, <= 1kB)
    all  : bool, écrire pour tous les robots du groupe
    team : int ou None, écrire pour une équipe spécifique
    """
    params = {"idx": idx}
    if all:
        params["all"] = "true"
    if team is not None:
        params["t"] = team

    resp = req.post(
        f"{BASE_URL}/udta",
        params=params,
        data=data.encode("utf-8"),
        timeout=TIMEOUT
    )
    _check_response(resp)


## Lecture dans un registre
def lecture(idx, team=None):
    """
    idx : registre [1..5]
    team : équipe à lire (None = équipe courante)
    """
    params = {"idx": idx}
    if team is not None:
        params["t"] = team

    resp = req.get(
        f"{BASE_URL}/udta",
        params=params,
        timeout=TIMEOUT
    )
    _check_response(resp)
    return resp.text

def capture_drapeau(id, sect, inner):
    """ Envoie de la capture d'un drapeau.

    Args:
        id (int): entier entre 5 et 16.
        sect (str): lettre entre A et H.
        inner (int): 1 pour le cercle intérieur et 0 pour le cercle extérieur.
    """
    reponse = req.post(f"{BASE_URL}/marker?id={id}&sector={sect}&inner={inner}")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")
    return reponse


def get_list() -> list[int]:
    """ Récupère la liste des balises à capturer.

    Returns:
        int list : les id des balises à capturer. 
    """
    try :
        reponse = req.get(f"{BASE_URL}/list")
        if reponse.status_code != 200:
            raise RuntimeError("Failed to get list from server")
        reponse = reponse.json()
        return reponse["markers"]
    except Exception as e:
        print(f"Error fetching list: {e}")
        return []
    
def post_pos(x=0, y=0, angle=0, id_groupe=0):
    """ Envoie de la position au serveur.

    Args:
        x (int, optional): Coordonnées x où le robot se trouve. Defaults to 0.
        y (int, optional): Coordonnées y où le robot se trouve. Defaults to 0.
        angle (int, optional): Angle par rapport à la balise en (1,5; 0). Defaults to 0.
        id_groupe (int, optional): Paramètre à mettre à 7 pour l'évaluation intermédiaire. Defaults to 0.
    """
    if id_groupe == 7:
        reponse = req.post(f"{BASE_URL}/pos?x={x}&y={y}&angle={angle}")
        print(f"Response from server: {reponse.status_code} - {reponse.text}")
    else:
        req.post(f"{BASE_URL}/pos?x={x}&y={y}&angle={angle}")