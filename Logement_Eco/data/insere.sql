-- Insertion de Codes Postaux
INSERT INTO Ville (Code, Nom) VALUES
(75001, 'Paris 1er'),
(75016, 'Paris 16e'),
(75011, 'Paris 11e');

-- Insertion de Adresses
INSERT INTO Adresse (Numero, Voie, Nom_voie, Code) VALUES
(123, 'Rue', 'de Paris', 75001),
(45, 'Avenue', 'Victor Hugo', 75016),
(8, 'Boulevard', 'Voltaire', 75011);

-- Insertion de Logements
INSERT INTO Logement (id_adresse, numero_telephone, adresse_ip, created_at) VALUES
(1, '+33 1 23 45 67 89', '192.168.1.100', '2024-01-01 10:00:00'),
(3, '+33 1 98 76 54 32', '192.168.1.101', '2024-01-02 11:30:00'),
(2, '+33 1 45 67 89 01', '192.168.1.102', '2024-01-03 14:15:00');

-- Insertion de Pièces
INSERT INTO Piece (id_l, nom, loc_x, loc_y, loc_z, created_at) VALUES
(1, 'Salon', 0.0, 0.0, 0.0, '2024-01-01 10:30:00'),
(1, 'Cuisine', 3.0, 0.0, 0.0, '2024-01-01 10:31:00'),
(1, 'Chambre', 0.0, 3.0, 0.0, '2024-01-01 10:32:00'),
(2, 'Salon', 0.0, 0.0, 0.0, '2024-01-02 12:00:00'),
(2, 'Cuisine', 4.0, 0.0, 0.0, '2024-01-02 12:01:00'),
(3, 'Salon', 0.0, 0.0, 0.0, '2024-01-03 14:30:00');

-- Insertion de Types de Capteurs
INSERT INTO Type_Capteur (nom, unite_mesure, description) VALUES
('Température', '°C', 'Capteur de température ambiante'),
('Humidité', '%', 'Capteur d''humidité relative'),
('Électricité', 'kWh', 'Compteur électrique'),
('Eau', 'm³', 'Compteur d''eau');

-- Insertion de Capteurs
INSERT INTO Capteur (id_tc, id_p, ref_commerciale, precision_min, precision_max, port_comm, created_at) VALUES
(1, 1, 'TEMP-001', -10.00, 50.00, 'COM3', '2024-01-01 11:00:00'),
(1, 2, 'TEMP-002', -10.00, 50.00, 'COM4', '2024-01-01 11:01:00'),
(2, 1, 'HUM-001', 0.00, 100.00, 'COM5', '2024-01-01 11:02:00'),
(3, 4, 'ELEC-001', 0.00, 10000.00, 'COM6', '2024-01-02 12:30:00'),
(4, 5, 'EAU-001', 0.00, 1000.00, 'COM7', '2024-01-02 12:31:00');

-- Insertion de Mesures
INSERT INTO Mesure (id_c, valeur, created_at) VALUES
(1, 21.5, '2024-01-01 12:00:00'),
(1, 22.0, '2024-01-01 13:00:00'),
(2, 20.5, '2024-01-01 12:00:00'),
(3, 65.0, '2024-01-01 12:00:00'),
(4, 150.5, '2024-01-02 13:00:00'),
(5, 0.5, '2024-01-02 13:00:00');

-- Insertion de Types de Factures
INSERT INTO Type_Facture (nom, description) VALUES
('Électricité', 'Facture de consommation électrique'),
('Eau', 'Facture de consommation d''eau'),
('Gaz', 'Facture de consommation de gaz');

-- Insertion de Factures
INSERT INTO Facture (id_l, id_tc, date_facture, montant, valeur_consommee, created_at) VALUES
(1, 1, '2024-01-31', 85.50, 450.00, '2024-02-01 10:00:00'),
(1, 2, '2024-01-31', 45.20, 15.00, '2024-02-01 10:01:00'),
(2, 1, '2024-01-31', 92.30, 485.00, '2024-02-01 10:02:00'),
(3, 3, '2024-01-31', 65.80, 250.00, '2024-02-01 10:03:00');