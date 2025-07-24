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
```
Traitement du fichier : 3188507227.fit
Timestamp de début (RAW):  2020-01-07 19:20:06
SPORT : inline_skating       /      SOUS-SPORT : 0
Distance totale (km) : 27
Fichier exporté vers : done/2020-01-07_20h20_roller_27km.fit
################################################################

Traitement du fichier : 3150854010.fit
Timestamp de début (RAW):  2019-12-26 17:00:55
SPORT : cycling       /      SOUS-SPORT : 0
Distance totale (km) : 5
Fichier exporté vers : done/2019-12-26_18h00_velo_5km.fit
################################################################

Traitement du fichier : 3192714394.fit
Timestamp de début (RAW):  2020-01-08 08:00:50
SPORT : cycling       /      SOUS-SPORT : 0
Distance totale (km) : 3
Fichier exporté vers : done/2020-01-08_09h00_velo_3km.fit
################################################################
```


## Prérequis
- Python 3.x
- Modules Python :
  - `fitparse`
  - `pytz`
  - `zipfile`
  - `shutil`

Installez les dépendances avec :
```bash
pip install -r requirements.txt
```
ou
```bash
pip install fitparse pytz
```

## Utilisation
Placez vos fichiers `.fit` dans le même dossier que le script, puis lancez :
```bash
python3 GPS_fit_files_parsing.py
```

Les fichiers traités seront déplacés dans le dossier `done/` avec un nom explicite.
En cas d’erreur, le fichier sera renommé avec le préfixe `error_`.

## Personnalisation
Le script adapte certains noms de sports et sous-sports pour les rendre plus lisibles en français.
Vous pouvez modifier ou ajouter des remplacements dans les variables `sport` et `subsport` selon vos besoins.