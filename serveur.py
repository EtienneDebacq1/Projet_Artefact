import http.server
import json             
from src.wattmetre import wattmetre
from urllib.parse import urlparse, parse_qs
from src.operations_usuelles import start
from src.manuel import stop_moteur_loop, avancer
import threading

mode = 0  # 0 = manuel, 1 = autonome

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/static/"):
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/':
            self._set_headers(200)
            with open('interface_yoan.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        elif self.path.startswith('/api/status'):
            self._set_headers(200)
            data = {
                "info": "Robot prêt",
                "level": 73
            }
            self.wfile.write(bytes(str(data), 'utf-8'))
            return
        elif self.path.startswith('/data'):
            data = {
                "tension": round(wattmetre.ina.get_bus_voltage_V(), 2),
                "courant": round(wattmetre.ina.get_current_mA() / 1000.0, 3),  # en A
            }

            body = json.dumps(data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)
            return
        else:
            self._set_headers(404)

    def do_POST(self):
        global mode 
        if self.path.startswith('/api/move'):
            parsed_url = urlparse(self.path)
            direction = parse_qs(parsed_url.query).get('dir', [''])[0]
            print(f"Commande reçue : {direction}")
            avancer(direction)
            self._set_headers(200)
        elif self.path.startswith('/api/mode'):
            self._set_headers(200)
            mode = 1
            stop_moteur_loop()
            threading.Thread(target=start, daemon=True).start()
        #edit yoan 
        if self.path.startswith('/api/test/move_30'):
            print("➡️ REQUÊTE TEST : Avance 30cm")
    
           
            try:
                  # <--- ON FORCE L'IMPORT ICI
                print("✅ Module wattmetre chargé")
            except Exception as e:
                print(f"❌ IMPOSSIBLE D'IMPORTER WATTMETRE: {e}")
                self.send_response(500)
                return
            # -----------------------

            try:
                # Maintenant Python connait forcément "wattmetre"
                avancer(30) 
                
                # 4. Envoi de la réponse
                reponse = {
                    "status": "succes",
                    "action": "Avancer 30cm",
                    "consommation": wattmetre.ina.get_power_mW(),
                    "unite": "Joules"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(reponse).encode('utf-8'))
                
            except Exception as e:
                print(f"ERREUR: {e}")
                self.send_response(500)
            
            return # Important pour ne pas exécuter le reste de do_POST


        else:
            self._set_headers(400)

PORT = 8080
server = http.server.HTTPServer(('', PORT), MyHandler)
print(f"Serveur en cours d'exécution sur le port {PORT}")
server.serve_forever()