#!/bin/bash

pkill -f "python3 serveur.py"

source venv/bin/activate

# Lancer python3 serveur.py en arrière-plan
python3 -u serveur.py

echo "Serveur lancé en arrière-plan avec le PID : $!"