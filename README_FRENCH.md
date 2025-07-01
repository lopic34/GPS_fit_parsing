# GPS_fit_files_parsing.py

Ce script permet de traiter et renommer automatiquement un lot de fichiers `.fit` (fichiers d’activité GPS, typiquement issus de montres ou compteurs sportifs Garmin, Suunto...) selon leur contenu, en extrayant des informations clés comme le sport, la distance, et la date de début d’activité.

## Fonctionnalités
- Parcourt tous les fichiers `.fit` du dossier courant.
- Extrait les informations de session et d’événement (sport, sous-sport, distance totale, timestamp de début).
- Renomme chaque fichier selon le format :
  `YYYY-MM-DD_HHhMM_<sport ou sous-sport>_<distance>km.fit`
- Traduit le nom de sport en français
- Déplace les fichiers traités dans un sous-dossier `done/`.
- Gère les erreurs de parsing ou de renommage en préfixant le fichier par `error_`.

## Exemple de fichiers de sorties
`2022-04-05_18h24_velo_11km.fit`
`2022-04-05_08h57_velo_11km.fit`
`2022-04-04_15h28_roller_10km.fit`
`2022-04-02_15h12_marche_3km.fit`
`2022-03-30_18h43_velo_9km.fit`
`2022-03-30_08h57_velo_11km.fit`
`2022-03-29_18h38_velo_6km.fit`

## Exemple log (journal d'exécution)
```Processing file: 2-sports-site-9565535999999605792.fit
SPORT:  running
SUB-SPORT:  0
Start Event Timestamp (RAW):  2025-02-03 11:25:17
total_distance_km:  8
File moved to: done/2025-02-03_12h25_running_8km.fit
###########################################

Processing file: 32-sports-site-956553599999960b5a4ebcf.fit
SPORT:  inline_skating
SUB-SPORT:  0
Start Event Timestamp (RAW):  2018-11-11 11:14:57
total_distance_km:  23
File moved to: done/2018-11-11_12h14_roller_23km.fit
###########################################

Processing file: 25-sports-site-95655359999996001714c77.fit
SPORT:  running
SUB-SPORT:  0
Start Event Timestamp (RAW):  2020-06-14 16:47:41
total_distance_km:  9
File moved to: done/2020-06-14_18h47_running_9km.fit
###########################################
```


## Prérequis
- Python 3.x
- Modules Python :
  - `fitparse`
  - `pytz`

Installez les dépendances avec :
```bash
pip install fitparse pytz
```
ou
```bash
pip install -r requirements.txt
```

## Utilisation
Placez vos fichiers `.fit` dans le même dossier que le script, puis lancez :
```bash
python GPS_fit_files_parsing.py
```

Les fichiers traités seront déplacés dans le dossier `done/` avec un nom explicite.
En cas d’erreur, le fichier sera renommé avec le préfixe `error_`.

## Personnalisation
Le script adapte certains noms de sports et sous-sports pour les rendre plus lisibles en français.
Vous pouvez modifier ou ajouter des remplacements dans les variables `sport` et `subsport` selon vos besoins.