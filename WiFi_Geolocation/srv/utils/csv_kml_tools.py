import xml.etree.ElementTree as ET
import csv

def parse_kml_to_csv(kml_file, csv_file):
    # Definindo os cabeçalhos do CSV
    csv_header = ["MAC", "SSID", "RSSI", "CurrentLatitude", "CurrentLongitude", "AltitudeMeters", "AccuracyMeters", "Type"]
    
    # Parse do arquivo KML
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    # Definindo o namespace KML
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Criando o arquivo CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8',) as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(csv_header)
        
        # Percorrendo todos os elementos de Placemark dentro de 'Document'
        for placemark in root.findall('.//kml:Placemark', namespace):
            # Pegando a descrição do Placemark e verificando o tipo
            description = placemark.find('kml:description', namespace)
            if description is not None:
                lines = description.text.splitlines()
                info = {line.split(": ")[0]: line.split(": ")[1] for line in lines if ": " in line}

                # Pegando apenas pontos de acesso do tipo "WIFI"
                if info.get("Type") == "WIFI":
                    # Extraindo valores necessários
                    mac = info.get("Network ID", "N/A")
                    ssid_elem = placemark.find('kml:name', namespace)
                    ssid = ssid_elem.text if ssid_elem is not None else "N/A"
                    ssid = ssid.replace("(no SSID)", "")
                    rssi = info.get("Signal", "N/A")
                    accuracy = info.get("Accuracy", "N/A")
                    
                    # Pegando coordenadas
                    coordinates = placemark.find('.//kml:coordinates', namespace)
                    if coordinates is not None:
                        lon, lat, *_ = coordinates.text.split(',')
                    
                    # Escrevendo no CSV
                    writer.writerow([mac, ssid, rssi, lat, lon, "N/A", accuracy, "WIFI"])

def csv_to_kml(csv_file, kml_file):
    # Open CSV file for reading
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Open KML file for writing
        with open(kml_file, 'w') as kmlfile:
            kmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            kmlfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            kmlfile.write('<Document>\n')
            for row in csvreader:
                # Extract relevant columns
                lat, lon = row['trilat'], row['trilong']
                network_id = row['id']
                # Write Placemark with relevant information
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
    # Iterate over files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            csv_file = os.path.join(input_dir, file_name)
            kml_file = os.path.join(input_dir, os.path.splitext(file_name)[0] + '.kml')
            csv_to_kml(csv_file, kml_file)



# Arquivos de entrada e saída
kml_file = '20241004-00363.kml'  # Substituir pelo nome do arquivo KML
csv_file = 'output.csv'   # Nome do arquivo CSV gerado

# Chamando a função para converter o KML em CSV
parse_kml_to_csv(kml_file, csv_file)
