import requests as req
import json
import http.server
from urllib.parse import urlparse, parse_qs

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
    else:
        req.post(f"{URL}/pos?x={x}&y={y}&angle={angle}")


def get_list():
    """ Récupère la liste des balises à capturer.

    Returns:
        int list : les id des balises à capturer. 
    """
    try :
        r = req.get(f"{URL}/list").json()
        return r["markers"][0]
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
    reponse =req.post(f"{URL}/marker?id={id}&sector={sect}&inner={inner}")
    print(f"Response from server: {reponse.status_code} - {reponse.text}")


def get_pos():
    """ Vérifie si le drapeau est validé.

    Returns:
        bool: rien si pas validé, false si en attente de validation et true si validé.
    """
    positions = (req.get(f"{URL}/status").json()[0])["position"]
    if not positions:
        return (0, 0, 0)
    p = positions[-1]
    return (p["x"], p["y"], p["theta"])


def post_start():
    """ Commence la course. 
    """
    req.post(f"{URL}/start")


def post_stop():
    """ Termine la course.
    """
    req.post(f"{URL}/stop")


def post_pattern(N):
    """ Choisi le motif de course N. Ne peut pas être changé en pleine course.
    """
    req.post(f"{URL}/pattern?idx={N}")


def get_pattern():
    """ Récupère le motif de parcours choisi.

    Returns:
        liste de balises : celle choisie par le motif.
    """
    r = req.get(f"{URL}/pattern").json()[0]
    return (r["markers"]["id"], r["markers"]["s"], r["markers"]["i"])


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


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()


    def do_GET(self):
        parsed = urlparse(self.path)

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
            return

        if parsed.path == "/api/status":
            x, y, angle = get_pos()
            response = {"etat": "pret", "x": x, "y": y, "angle": angle}
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode())
            return

        if parsed.path == "/api/pattern/get":
            id, sect, inner = get_pattern()
            self._set_headers(200)
            self.wfile.write(json.dumps({"id": id, "secteur": sect, "inner": inner}).encode())
            return

        if parsed.path == "/api/flags/get":
            flag = get_list()
            self._set_headers(200)
            self.wfile.write(json.dumps(flag).encode())
            return

        if parsed.path == "/api/maj/get":
            qs = parse_qs(parsed.query)
            rid = int(qs.get("id", [1])[0])
            tid = int(qs.get("team", [0])[0])
            val = get_maj(rid, tid)
            self._set_headers(200)
            self.wfile.write(json.dumps(val).encode())
            return

        # Pas trouvé
        self._set_headers(404)
        self.wfile.write(b'{"error": "Not found"}')


    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/move":
            direction = parse_qs(parsed.query).get("dir", [""])[0]

            if direction == "up":
                post_pos(0, 50, 0, 7)
            elif direction == "down":
                post_pos(0, -50, 180, 7)
            elif direction == "left":
                post_pos(-50, 0, 270, 7)
            elif direction == "right":
                post_pos(50, 0, 90, 7)

            self._set_headers(200)
            self.wfile.write(b'{"ok": true}')
            return

        if parsed.path == "/api/start":
            post_start()
            self._set_headers(200)
            self.wfile.write(b'{"started": true}')
            return

        if parsed.path == "/api/stop":
            post_stop()
            self._set_headers(200)
            self.wfile.write(b'{"stopped": true}')
            return

        if parsed.path == "/api/pattern":
            qs = parse_qs(parsed.query)
            idx = int(qs.get("id", [0])[0])
            post_pattern(idx)
            self._set_headers(200)
            self.wfile.write(b'{"pattern_set": true}')
            return

        if parsed.path == "/api/pos":
            qs = parse_qs(parsed.query)
            x = int(qs.get("x", [0])[0])
            y = int(qs.get("y", [0])[0])
            angle = int(qs.get("angle", [0])[0])
            post_pos(x, y, angle)
            self._set_headers(200)
            self.wfile.write(b'{"pos_sent": true}')
            return

        if parsed.path == "/api/flags/set":
            qs = parse_qs(parsed.query)
            id = int(qs.get("id", [0])[0])
            sector = qs.get("sector", ["A"])[0]
            inner = int(qs.get("inner", [1])[0])
            post_list(id, sector, inner)
            self._set_headers(200)
            self.wfile.write(b'{"flag_sent": true}')
            return

        if parsed.path == "/api/maj/set":
            qs = parse_qs(parsed.query)
            rid = int(qs.get("id", [1])[0])
            val = qs.get("val", ["false"])[0] == "true"
            tid = int(qs.get("team", [0])[0])
            post_maj(rid, val, tid)
            self._set_headers(200)
            self.wfile.write(b'{"maj_sent": true}')
            return

        # ----------- Erreur ----------
        self._set_headers(400)
        self.wfile.write(b'{"error": "Bad request"}')


if __name__ == "__main__":
    PORT = 8080
    server = http.server.HTTPServer(('', PORT), MyHandler)
    print(f"Serveur opérationnel sur http://localhost:{PORT}")
    server.serve_forever()
