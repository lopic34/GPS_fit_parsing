import fitparse
import os
import glob
from datetime import datetime
import pytz # gestion de timezone

def parse_fit_file(file_path):
    fitfile = fitparse.FitFile(file_path)
    session_data = []
    event_data = []

    for message in fitfile.get_messages():
        if message.name == 'session':
            session = {}
            for data in message:
                session[data.name] = data.value
            session_data.append(session)
        elif message.name == 'event':
            event = {}
            for data in message:
                event[data.name] = data.value
            event_data.append(event)

    return session_data, event_data

# Get all .fit files in the directory
fit_files = glob.glob('*.fit')

for file_path in fit_files:
    print(f"Processing file: {file_path}")
    try:
        sessions, events = parse_fit_file(file_path)

        for session in sessions:
            print("SPORT: ", session.get('sport', 0))
            print("SUB-SPORT: ", session.get('sub_sport', 0))
            #print("EVENT: ", events)
            start_event_timestamp = None
            for event in events:
                if event.get('event_type') == 'start':
                    start_event_timestamp = event.get('timestamp')
                    break  # Sortir de la boucle après avoir trouvé le premier événement de type start
            # Afficher le premier timestamp des événements de type start
            if start_event_timestamp:
                print("Start Event Timestamp (RAW): ", start_event_timestamp)
                # Convertir en heure de UTC et Paris
                utc_tz = pytz.timezone('UTC')
                paris_tz = pytz.timezone('Europe/Paris')
                if start_event_timestamp.tzinfo is None:
                    start_event_timestamp = utc_tz.localize(start_event_timestamp)
                start_event_timestamp_paris = start_event_timestamp.astimezone(paris_tz)
                formatted_timestamp = start_event_timestamp_paris.strftime('%Y-%m-%d_%Hh%M')
                #print("Start Event Timestamp (Paris Time): ", formatted_timestamp)

            total_distance = session.get('total_distance', 0)  # Valeur par défaut de 0 si la clé n'existe pas
            if total_distance != 0:
                total_distance_km = int(total_distance / 1000)
            else:
                total_distance_km = 0 
            print("total_distance_km: ", total_distance_km)
            # Formater la date au format yyyy-mm-dd_hh_mm

            # Convertir session['sport'] en chaîne de caractères avant d'appeler replace
            sport = str(session.get('sport', 0))
            sport = sport.replace('inline_skating', 'roller').replace('cycling', 'velo').replace('walking', 'marche').replace('hiking', 'randonnee').replace('cross_country_skiing', 'ski_de_fond').replace('snowboarding', 'snowboard').replace('snowshoeing','raquettes_neige').replace('swimming', 'natation').replace('64','badbimton')

            subsport = str(session.get('sub_sport', 0))
            subsport = subsport.replace('mountain', 'vtt').replace('hiking', 'randonnee').replace('85','padel')
        
            # Concaténer les variables sport, total_distance_km et la date formatée
            try:
                if subsport == "0" or subsport == 0:
                    new_file_name = f"{formatted_timestamp}_{sport}_{total_distance_km}km.fit"
                else:
                    new_file_name = f"{formatted_timestamp}_{subsport}_{total_distance_km}km.fit"

                # Créer le sous-répertoire "done" s'il n'existe pas
                done_dir = os.path.join(os.path.dirname(file_path), 'done')
                os.makedirs(done_dir, exist_ok=True)

                # Déplacer le fichier dans le sous-répertoire "done"
                new_file_path = os.path.join(done_dir, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"File moved to: {new_file_path}")
                print("###########################################\n")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                # Renommer le fichier avec un préfixe error_
                error_file_name = f"error_{file_path}"
                error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
                os.rename(file_path, error_file_path)
                print(f"File renamed to: {error_file_path}")
                print("###########################################\n")

    except Exception as e:
        print(f"Erreur lors du parsing du fichier {file_path}: {e}")
        # Renommer le fichier avec un préfixe error_
        error_file_name = f"error_{os.path.basename(file_path)}"
        error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
        os.rename(file_path, error_file_path)
        print(f"Fichier renommé en : {error_file_path}")
        print("###########################################\n")
        continue  # Passer au fichier suivant