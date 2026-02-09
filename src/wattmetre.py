# -*- coding: utf-8 -*-
import sys
import time
import threading

from DFRobot_INA219.Python.RespberryPi.DFRobot_INA219 import INA219 


class Wattmetre:
    def __init__(self):
        self._thread = None
        self._en_cours = False
        self.energie_joules = 0.0
        self.ina = None
        
        try:
            self.ina = INA219(8, INA219.INA219_I2C_ADDRESS4)
            
            # Tentative d'initialisation (non-bloquante pour ne pas figer le serveur)
            if not self.ina.begin():
                print("⚠️ Wattmètre: Init échouée (Vérifier câbles/ADR)")
            else:
                # Tes paramètres de calibration
                self.ina.linear_cal(1000, 1000)
                print("✅ Wattmètre initialisé et calibré.")
                
        except Exception as e:
            print(f"⚠️ Erreur Hardware Wattmètre : {e}")

    def _boucle_mesure(self):
        """Cette fonction tourne en arrière-plan pendant que le robot avance"""
        temps_precedent = time.time()
        
        while self._en_cours and self.ina:
            try:
                temps_actuel = time.time()
                dt = temps_actuel - temps_precedent
                
                # --- TA LECTURE DE PUISSANCE ---
                puissance_mW = self.ina.get_power_mW()
                
                # Conversion en Joules (Energie = Puissance_W * Temps_s)
                # On divise par 1000 car on reçoit des mW
                energie_instant = (puissance_mW / 1000.0) * dt
                self.energie_joules += energie_instant
                
                temps_precedent = temps_actuel
                time.sleep(0.05) # On mesure 20 fois par seconde
                
            except Exception as e:
                print(f"Erreur lecture I2C: {e}")
                # En cas d'erreur I2C, on essaie de continuer sans planter

    def demarrer(self):
        """Lance l'enregistrement"""
        self.energie_joules = 0.0
        self._en_cours = True
        self._thread = threading.Thread(target=self._boucle_mesure)
        self._thread.start()
        print("⚡ Mesure démarrée...")

    def arreter_et_recuperer(self):
        """Arrête l'enregistrement et renvoie le total"""
        self._en_cours = False
        if self._thread:
            self._thread.join()
        
        print(f"⚡ Fin mesure. Conso totale : {self.energie_joules:.2f} Joules")
        return round(self.energie_joules, 2)

# On crée une instance unique pour que le serveur puisse l'utiliser
wattmetre = Wattmetre()