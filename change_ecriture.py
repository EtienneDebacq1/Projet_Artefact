import src.server_commun as serv
import json

def reset_sector(id_robot):
    old_registre = json.loads(serv.lecture(id_robot))
    old_registre["used_sector"] = []
    new_text = json.dumps(old_registre)
    serv.ecriture(id_robot, new_text, True)

if __name__ == "__main__":
    id_robot = int(input("Enter robot ID to reset sectors: "))
    reset_sector(id_robot)