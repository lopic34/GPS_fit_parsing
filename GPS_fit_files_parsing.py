import fitparse
import os
import glob
from datetime import datetime
import pytz # gestion de timezone
import zipfile
import shutil

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


def process_fit_files_in_root(selected_lang):
    fit_files = glob.glob('*.fit')
    for file_path in fit_files:
        if selected_lang == 'fr':
            print(f"Traitement du fichier : {file_path}")
        else:
            print(f"Processing file: {file_path}")
        try:
            sessions, events = parse_fit_file(file_path)

            for session in sessions:
                start_event_timestamp = None
                for event in events:
                    if event.get('event_type') == 'start':
                        start_event_timestamp = event.get('timestamp')
                        break
                if start_event_timestamp:
                    if selected_lang == 'fr':
                        print("Timestamp de début (UTC RAW): ", start_event_timestamp)
                    else:
                        print("Start Event Timestamp (RAW): ", start_event_timestamp)
                    utc_tz = pytz.timezone('UTC')
                    paris_tz = pytz.timezone('Europe/Paris')
                    if start_event_timestamp.tzinfo is None:
                        start_event_timestamp = utc_tz.localize(start_event_timestamp)
                    start_event_timestamp_paris = start_event_timestamp.astimezone(paris_tz)
                    formatted_timestamp = start_event_timestamp_paris.strftime('%Y-%m-%d_%Hh%M')

                total_distance = session.get('total_distance', 0)
                if total_distance != 0:
                    total_distance_km = int(total_distance / 1000)
                else:
                    total_distance_km = 0
                if selected_lang == 'fr':
                    print("SPORT :", session.get('sport', 0), "      /      SOUS-SPORT :", session.get('sub_sport', 0))
                    print("Distance totale (km) :", total_distance_km)
                else:
                    print("SPORT: ", session.get('sport', 0), "      /      SUB-SPORT: ", session.get('sub_sport', 0))
                    print("Total_distance_km: ", total_distance_km)
                sport = str(session.get('sport', 0))
                sport = sport.replace('inline_skating', 'roller').replace('cycling', 'velo').replace('walking', 'marche').replace('hiking', 'randonnee').replace('cross_country_skiing', 'ski_de_fond').replace('snowboarding', 'snowboard').replace('snowshoeing','raquettes_neige').replace('swimming', 'natation').replace('64','badbimton')

                subsport = str(session.get('sub_sport', 0))
                subsport = subsport.replace('mountain', 'vtt').replace('hiking', 'randonnee').replace('85','padel')

                try:
                    if subsport == "0" or subsport == 0:
                        new_file_name = f"{formatted_timestamp}_{sport}_{total_distance_km}km.fit"
                    else:
                        new_file_name = f"{formatted_timestamp}_{subsport}_{total_distance_km}km.fit"

                    done_dir = os.path.join(os.path.dirname(file_path), 'done')
                    os.makedirs(done_dir, exist_ok=True)
                    new_file_path = os.path.join(done_dir, new_file_name)
                    os.rename(file_path, new_file_path)
                    if selected_lang == 'fr':
                        print(f"Fichier exporté vers : {new_file_path}")
                        print("################################################################\n")
                    else:
                        print(f"File exported to: {new_file_path}")
                        print("################################################################\n")

                except Exception as e:
                    if selected_lang == 'fr':
                        print(f"Erreur lors du traitement du fichier {file_path} : {e}")
                        error_file_name = f"error_{file_path}"
                        error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
                        os.rename(file_path, error_file_path)
                        print(f"Fichier renommé en : {error_file_path}")
                        print("###########################################\n")
                    else:
                        print(f"Error processing file {file_path}: {e}")
                        error_file_name = f"error_{file_path}"
                        error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
                        os.rename(file_path, error_file_path)
                        print(f"File renamed to: {error_file_path}")
                        print("###########################################\n")

        except Exception as e:
            if selected_lang == 'fr':
                print(f"Erreur lors du parsing du fichier {file_path} : {e}")
                error_file_name = f"error_{os.path.basename(file_path)}"
                error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
                os.rename(file_path, error_file_path)
                print(f"Fichier renommé en : {error_file_path}")
                print("###########################################\n")
            else:
                print(f"Error parsing file {file_path}: {e}")
                error_file_name = f"error_{os.path.basename(file_path)}"
                error_file_path = os.path.join(os.path.dirname(file_path), error_file_name)
                os.rename(file_path, error_file_path)
                print(f"File renamed to: {error_file_path}")
                print("###########################################\n")
            continue

def extract_and_process_zip(zip_path, extract_dir, selected_lang):
    if selected_lang == 'fr':
        print(f"Extraction du zip {zip_path} dans {extract_dir}")
    else:
        print(f"Extracting zip {zip_path} to {extract_dir}")
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    activities_dir = os.path.join(extract_dir, 'activities')
    if os.path.exists(activities_dir):
        for file in os.listdir(activities_dir):
            if file.endswith('.fit.gz'):
                src = os.path.join(activities_dir, file)
                dst = os.path.join(os.getcwd(), file[:-3])
                try:
                    import gzip
                    with gzip.open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    if selected_lang == 'fr':
                        print(f"Décompresse {src}")
                    else:
                        print(f"Decompressing {src}")
                except Exception as e:
                    if selected_lang == 'fr':
                        print(f"Erreur lors de la décompression de {src} : {e}")
                    else:
                        print(f"Error decompressing {src}: {e}")
    else:
        if selected_lang == 'fr':
            print(f"Le dossier {activities_dir} n'existe pas ou ne contient pas de fichiers .fit.gz.")
        else:
            print(f"Directory {activities_dir} does not exist or contains no .fit.gz files.")
    process_fit_files_in_root(selected_lang)

def main():
    print("Choisissez la langue / Choose language :")
    print("1 : Français")
    print("2 : English")
    lang_choice = input("Votre choix / Your choice (1 ou 2): ")
    if lang_choice == "1":
        selected_lang = 'fr'
    else:
        selected_lang = 'en'

    if selected_lang == 'fr':
        print("Choisissez une option :")
        print("1 : Traiter tous les fichiers .fit du répertoire racine")
        print("2 : Extraire le zip, copier les fichiers extraits dans le répertoire racine, puis traiter les fichiers .fit")
        choix = input("Votre choix (1 ou 2) : ")
    else:
        print("Choose an option:")
        print("1 : Process all .fit files in the root directory")
        print("2 : Extract the zip, copy extracted files to root, then process .fit files")
        choix = input("Your choice (1 or 2): ")

    if choix == "1":
        process_fit_files_in_root(selected_lang)
    elif choix == "2":
        # Supprimer les fichiers .fit du répertoire racine avant extraction
        for file in os.listdir(os.getcwd()):
            if file.endswith('.fit'):
                try:
                    os.remove(file)
                    if selected_lang == 'fr':
                        print(f"Suppression ancien fichier : {file}")
                    else:
                        print(f"Deleted old file: {file}")
                except Exception as e:
                    if selected_lang == 'fr':
                        print(f"Erreur lors de la suppression de {file} : {e}")
                    else:
                        print(f"Error deleting {file}: {e}")
        zip_path = 'Strava_130725export_49229515.zip'
        extract_dir = 'extracted'
        extract_and_process_zip(zip_path, extract_dir, selected_lang)
    else:
        if selected_lang == 'fr':
            print("Choix invalide.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()