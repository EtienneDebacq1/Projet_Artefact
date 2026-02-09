import requests
import time

# --- CONFIGURATION ---
IP_ROBOT = "137.194.173.73"  # <--- METTRE L'IP DE TA RASPBERRY ICI
PORT = 8080
URL = f"http://{IP_ROBOT}:{PORT}/api/test/move_30"

def lancer_test_client():
    print(f"📡 Connexion au robot : {URL}")
    print("⏳ Envoi de l'ordre : Avancer 30cm + Mesurer conso...")
    
    try:
        depart = time.time()
        
        # On envoie la demande. Le timeout est à 20sec car le robot va bouger.
        reponse = requests.post(URL, timeout=20)
        
        duree_totale = time.time() - depart
        
        if reponse.status_code == 200:
            data = reponse.json()
            print("\n✅ TEST RÉUSSI !")
            print("====================================")
            print(f" Action réalisée : {data.get('action')}")
            print(f" Consommation    : {data.get('consommation')} {data.get('unite')}")
            print(f" Temps opération : {duree_totale:.2f} secondes")
            print("====================================")
        else:
            print(f"❌ Erreur Serveur (Code {reponse.status_code})")
            print("Message:", reponse.text)

    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter. Vérifie l'IP et que server.py tourne.")
    except requests.exceptions.Timeout:
        print("❌ Le robot met trop de temps à répondre.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    lancer_test_client()