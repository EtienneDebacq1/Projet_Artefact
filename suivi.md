# Suivi de projet

## Descriptif

- Groupe 7 Équipe 3
- Nom d'équipe: MEYE

### Membres:

- Marius ALBERT
- Yoan FRANCOIS
- Eva HERSON
- Etienne DEBACQ

### Forces et faiblesses:

Force = motivation
Faiblesse = 2 personnes n'ont jamais fait d'informatique

## Répartition des tâches et Planning initial

Indiquez le responsable de la tâche et **les dates** estimées pour les versions suivantes:

- **V0**: premiers exemples pour tester et expérimenter, sans structure bien définie
- **V1**: code fonctionnel, structuré mais indépendant des autres tâches
- **V2**: code fonctionnel intégré à l'ensemble

Le responsable de tâche doit s'assurer que les dates sont respectées. Il n'est pas nécessairement le seul à travailler sur cette tâche.

**Attention**:
- Il faut un unique responsable par tâche
- La complétion de chaque tâche à la date indiquée sera vérifiée (tuteur / jury)
- Si vous **ajoutez une tâche** supplémentaire, pensez à **valider avec votre tuteur**

| Tâche                 | Responsable   | V0 (prévu) | V0 (réalisé) | V1 (prévu) | V1 (réalisé) | V2 (prévu) | V2 (réalisé) |
| -------               | ------------- | ----       | ----         | ----       | ----         | ---        | ---          |
| Conception robot      | Groupe        | 26/09       | 26/09         | 14/10       | 18/11         | 18/12        | N/A          |
| Config. Rasberry      | Etienne           | 30/09       | 30/09         | 14/10       | 14/10         | N/A        | N/A          |
| Contrôle déplacements | Marius           | 14/10       | 24/10         | 12/11       | 18/11         | 18/11       | 18/11         |
| Logique ctrl et suivi | Etienne           | 14/10       | 24/10         | 12/11       | 18/11         | 18/11       | 19/11         |
| Interface. Web ctrl   | Yoan           | 14/10       | 14/10         | 24/10       | 24/10         | 18/11       | 18/11         |
| Détection balises     | Eva           | 14/10       | 24/10         | 24/10       | 11/10         | 18/11       | 19/11         |

**Attention**:
Pour la conception du robot, vous devrez:

- avoir votre plan au format **SVG** sur votre dépôt Git, en racine sous le nom **`plan_decoupe_GR_EQ.svg`** avec `GR` votre numéro de groupe et `EQ` votre numéro d'équipe;
- faire **valider** votre plan par votre **tuteur** (en séance ou hors séance);
- après validation, envoyer un mail à [**M. Bouhier**](mailto:mickael.bouhier@telecom-paris.fr) pour faire votre demande de découpe.

Ce plan devra être en ligne **au plus tard le 24/10/2025, sachant que le délai avant découpe est d'environ une semaine**.

*Note pour tuteur*: vérifier que le fichier est bien sur le Git.


## Planning final

**À compléter après l'évaluation intermédiaire**

Donnez par tâche les prochaines étapes et **tests** envisagés pour l'épreuve collaborative.
Ces tests ne sont pas nécessairement les mêmes que ceux des autres équipes du groupe.
Vous pouvez ajouter plusieurs entrées par tâche.

Les responsables des tâches définies dans le planning initial sont responsables des tests correspondants. Tout changement **doit être discuté et validé avec le tuteur**.


| Tâche                 | Responsable | Détails                                           | Date (prévu)   | Date (réalisé)      |
| ---------             | ---------   | ---------                                         | --------       | --------  |
| Contrôle déplacements | Marius     | Corriger dérive droite du robot                   | À Remplir      | À Remplir |
| Contrôle déplacements | Marius     | Mise en place **tests de déplacement**            | À Remplir      | À Remplir |
| Serveur Web           | Eva     | Corriger bug bascule mode autonome et mode manuel | À Remplir      | À Remplir |
| Interface Web         | Yoan     | Améliorer réactivité pour pilotage manuel         | À Remplir      | À Remplir |
| Interface Web         | Eva     | Corriger bugs d'affichage des logs                | À Remplir      | À Remplir |
| Détection balises     | Eva     | Diminuer latence dans le traitement               | À Remplir      | À Remplir |
| Détection balises     | Eva     | Mise en place **tests positionnement**            | À Remplir      | À Remplir |
| Logique ctrl. et suivi | Etienne | Corriger l'envoie des balises au serveur         | 10/01      | 14/01 |


## Architecture

Détaillez ici l'architecture logicielle de votre programme **aux deux étapes d'évaluations**.
Vous pouvez vous appuyer sur un schéma.

Notez en particulier:

- les différentes phases algorithmiques (capture image, calibration, commandes moteurs, requêtes HTTP)
- le séquencement de ces phases (utilisation de _threads_, de _process_ indépendants, de tâches discrètes)
- le cas échéant, comment vos différents modules échangent-ils les données (via fichiers, sockets, objets partagés) et comment la concurrence entre threads/process est-elle gérée.

### Architecture évaluation intermédiaire

# Mode manuel
    interface web tourne sur la raspberry et appelle les fonctions de contrôle des déplacements
    quand on appuie sur un bouton, une requête est envoyée à la raspberry qui exécute la commande

# Mode automatique
    boucle principale dans automatique.py se déclanche quand on appuie sur "mode" dans l'interface web
    il avance un peu pour être au centre
    il cherche une balise, si il en trouve pas, il teste de se déclaler legerement vers la gauche puis vers la droite
    au bout de 7 secondes si il a pas trouvé il récupère dans getlist

    lorsque un balise cible il fait : 

    - il tourne tant qu'il ne la voit pas
    - quand il la voit, il calcule son angle et sa distance
    - si jamais il est a plus de 60 cm il avance 
    - si l'angle est à positif il tourne à gauche, sinon à droite
    - il répète jusqu'à être à 20 cm de la balise

    - il envoie la capture au serveur
    - il tourne sur lui même 
    - il recule un peu pour être au centre
    - il demande la prochaine balise cible
    - il recommence


### Architecture évaluation finale

**À compléter le moment venu**

## Tests


Détaillez dans cette section tous les tests mis en place pour valider votre code.
La forme est libre, mais vous devez documenter:

- ce que fait le test
- comment exécuter le test (ou une série de test) depuis la racine de votre dépôt Git.

Ces tests doivent vous permettre de valider rapidement qu'un bloc logiciel dans votre programme fonctionne comme prévu.
Il est donc **impératif** que le test utilise directement le code tel qu'utilisé dans votre programme, et non une copie de ce code.

Chaque tâche identifiée dans le planning initial **doit avoir** des tests associés. Pour la Raspberry, pensez à faire des scripts de réinstallation.

**Attention**, ces tests doivent:

- être exécutable de manière automatisée (si possible), c'est-à-dire sans intervention humaine autre que l'exécution de la ligne de commande initiale,
- pouvoir tourner sur n'importe quelle carte Raspberry, ne mettez aucun chemin de fichier en absolu dans votre code ou dans vos tests,
- si l'installation de dépendances particulières (par pip ou apt) pensez à l'indiquer ou ajouter un script de configuration initiale.

### Tests déplacement 

Pour la capacité à avancer: 

Lancement du test : 

```bash
python3 tests/avancer_test.py 
```

Que fait le test ? 
1er sous-test (test impulsion): le robot avance pendant 3 secondes, on mesure de combien de centimètres il a avancé puis on rentre cette valeur, le test nous renvoie le nombre d'impulsions/cm qu'il faut. Permet de calibrer.
2ème sous-test (test de la fonction avancer): on rentre la distance en centimètre et on mesure l'écart avec la distance réelle. 

Pour la capacité à tourner: 

Lancement du test :

```bash
python3 tests/tourner_test.py
```

Que fait le test ?
Fait tourner le robot de 15° dans un sens sélectionné entre gauche et droite (correspondant à 1 ou -1). Si un autre nombre est entré, on ne fait rien.

### Tests caméras 

Lancement du test :

```bash
python3 tests/camera_test.py
```

Que fait le test ?
1er sous-test (test_detect_markers) : la caméra capture une image, elle regarde si un aruco est présent, le test doit lui indiquer si oui ou non l'aruco est bien présent
2ème sous-test (test_calculate_distance_angle) : la caméra renvoie les informations de distance et d'angle du aruco présent, vérification manuelle de ces informations. 
Résultat : L'angle est les bon à 2 degré près et la distance à 5 cm environ.

### Tests serveur suivi 

Lancement du test :

```bash
python3 tests/server_suivi_test.py 
```

Toutes les commandes envoyées au serveur sont testées. On regarde la réponse du serveur et si il y'a une erreur. Le test stocke les informations de position des balises pour pouvoir envoyer les bonnes informations.



### Tests client-serveur web 

On envoie une requête pour avancer de 30cm et on récupère la consommation de la carte.

Lancement du test:

```bash
python3 test_web.py 
```



## Performances

*À compléter après l'évaluation intermédiaire, au plus tard pour l'évaluation finale*

**Par exemple:**

- Temps de traitement Caméra+Aruco en images par secondes : 25 images/s.
- Latence traitement Caméra+Aruco + action moteur : 100 ms.
- Latence moyenne des communications réseau (requêtes client/serveur, en local, en wifi, vers le serveur d'évaluation) : 130 ms.
- Latence traitement Caméra+Aruco + réponse serveur : 170 ms.
- Vitesse maximale de déplacement du robot en ligne droite, m/s : 0.6 m/s.
- Vitesse minimale de déplacement du robot en ligne droite, m/s >0 : 0.04 m/s.
- Charge CPU moyenne en pilotage manuel : 25%.
- Charge CPU moyenne en pilotage automatique : 65%.
- Consommation estimée en pilotage manuel : 5 W.
- Consommation estimée en pilotage automatique : 7 W.

## Bilans

*Le bilan décrit votre analyse de ce qui a marché, ce qui n'a pas fonctionné, ce qu'il faut ou faudrait corriger. Il est à compléter immédiatement après chaque évaluation.*

### Bilan évaluation intermédiaire

Notre robot marche mais nous avions un problème d'envoie des requêtes au serveur : celle de position. Nous envoyons None au lieu d'une lettre pour le secteur. Erreur modifiée.

### Bilan évaluation finale

#### Bilan Robot seul

Notre robot fonctionne bien et fait ce qui est demandé.

#### Bilan Coopération

Bonne entente même si certains groupes étaient plus investis que d'autres.

## Détail des Tâches

Notez pour chaque tâche les expertises externes que vous avez sollicitées (autres élèves du groupe, 1A, 2A, enseignants),
les ressources bibliographiques utilisées et toutes autres remarques sur son fonctionnement.

Notez en particulier les différentes pistes techniques envisagées,
leurs avantages et inconvénients et les raisons de vos choix techniques (simplicité, qualité de la documentation, tutos, expérience passée, ...).

--------------------

### Tâche: Conception du robot

#### Expertises

- Dr X. Pert

#### Bibliographie

- http://foo.com: tuto sur l'utilisation de _Inkscape_

#### Remarques & Fonctionnement

--------------------

### Tâche: Raspberry Pi, installation, configuration de la carte et l'environnement

#### Expertises
Eva

#### Bibliographie

#### Remarques & Fonctionnement

--------------------

### Tâche: Contrôle des déplacements

#### Expertises
Marius

#### Bibliographie

#### Remarques & Fonctionnement

--------------------

### Tâche: Logique de suivi et contrôle

#### Expertises
Etienne

#### Bibliographie

#### Remarques & Fonctionnement

--------------------

### Tâche: Interface Web de contrôle à distance

#### Expertises
Yoan

#### Bibliographie

#### Remarques & Fonctionnement

--------------------

### Tâche: Détection des balises

#### Expertises
Eva

#### Bibliographie

#### Remarques & Fonctionnement


--------------------

### Tâche de groupe: Architecture logicielle

#### Expertises
Etienne et Eva

#### Bibliographie

#### Remarques & Fonctionnement



## Suivi des séances

*Pour le suivi de vos séances, notez ce qui a été fait pendant la séance, et ce qui doit être préparé pour avant la prochaine séance.
La forme est libre, conservez juste le titre des séances (_TH X-Y_).*

### TH 1-2

#### Pendant la séance

- Présents: Eva, Yoan, Marius, Etienne
- Tâches: 
- Réflexion autour de la construction du robot. 

Idées : 
    - Roues motrices derrières

Logiciel : 
    - Inskape
    - Fusion 

Idées design :
    - chaussure
    - vaisseau star wars
    - sous-marin


#### À prévoir pour la prochaine séance

### TH 3-4

#### Pendant la séance

#### À prévoir pour la prochaine séance


**A compléter ...*
