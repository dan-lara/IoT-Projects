import xml.etree.ElementTree as ET
import csv

def parse_kml_to_csv(kml_file, csv_file):
    # Définir les en-têtes du CSV
    csv_header = ["MAC", "SSID", "RSSI", "CurrentLatitude", "CurrentLongitude", "AltitudeMeters", "AccuracyMeters", "Type"]
    
    # Analyser le fichier KML
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    # Définir l'espace de noms KML
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Créer le fichier CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8',) as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(csv_header)
        
        # Parcourir tous les éléments Placemark dans 'Document'
        for placemark in root.findall('.//kml:Placemark', namespace):
            # Obtenir la description du Placemark et vérifier le type
            description = placemark.find('kml:description', namespace)
            if description is not None:
                lines = description.text.splitlines()
                info = {line.split(": ")[0]: line.split(": ")[1] for line in lines if ": " in line}

                # Obtenir uniquement les points d'accès de type "WIFI"
                if info.get("Type") == "WIFI":
                    # Extraire les valeurs nécessaires
                    mac = info.get("Network ID", "N/A")
                    ssid_elem = placemark.find('kml:name', namespace)
                    ssid = ssid_elem.text if ssid_elem is not None else "N/A"
                    ssid = ssid.replace("(no SSID)", "")
                    rssi = info.get("Signal", "N/A")
                    accuracy = info.get("Accuracy", "N/A")
                    
                    # Obtenir les coordonnées
                    coordinates = placemark.find('.//kml:coordinates', namespace)
                    if coordinates is not None:
                        lon, lat, *_ = coordinates.text.split(',')
                    
                    # Écrire dans le CSV
                    writer.writerow([mac, ssid, rssi, lat, lon, "N/A", accuracy, "WIFI"])

def csv_to_kml(csv_file, kml_file):
    # Ouvrir le fichier CSV pour lecture
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Ouvrir le fichier KML pour écriture
        with open(kml_file, 'w') as kmlfile:
            kmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kmlfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kmlfile.write('<Document>\n')
            for row in csvreader:
                # Extraire les colonnes pertinentes
                lat, lon = row['trilat'], row['trilong']
                network_id = row['id']
                # Écrire Placemark avec les informations pertinentes
                kmlfile.write('<Placemark>\n')
                kmlfile.write('<name>{}</name>\n'.format(network_id))
                kmlfile.write('<description>ID: {}</description>\n'.format(network_id))
                kmlfile.write('<Point>\n')
                kmlfile.write('<coordinates>{},{},0</coordinates>\n'.format(lon, lat))
                kmlfile.write('</Point>\n')
                kmlfile.write('</Placemark>\n')
            kmlfile.write('</Document>\n')
            kmlfile.write('</kml>\n')

def convert_csv_files_to_kml(input_dir):
    # Itérer sur les fichiers dans le répertoire d'entrée
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            csv_file = os.path.join(input_dir, file_name)
            kml_file = os.path.join(input_dir, os.path.splitext(file_name)[0] + '.kml')
            csv_to_kml(csv_file, kml_file)

# # Fichiers d'entrée et de sortie
# kml_file = '20241004-00363.kml'  # Remplacer par le nom du fichier KML
# csv_file = 'output.csv'   # Nom du fichier CSV généré

# # Appeler la fonction pour convertir le KML en CSV
# parse_kml_to_csv(kml_file, csv_file)
