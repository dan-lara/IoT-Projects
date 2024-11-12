-- Désactive temporairement les clés étrangères pour la création des tables
PRAGMA foreign_keys = OFF;

-- Supprime les tables existantes si elles existent
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Type_Facture;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS Type_Capteur;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Adresse;
DROP TABLE IF EXISTS Ville;

-- Crée les tables
CREATE TABLE Ville (
    Code INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL
);

CREATE TABLE Adresse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Numero INTEGER NOT NULL,
    Voie TEXT NOT NULL,
    Nom_voie TEXT NOT NULL,
    Code INTEGER NOT NULL,
    FOREIGN KEY (Code) REFERENCES Ville(Code)
);

CREATE TABLE Logement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_adresse INTEGER NOT NULL,
    numero_telephone VARCHAR(20),
    adresse_ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_adresse) REFERENCES Adresse(id)
);

CREATE TABLE Piece (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_l INTEGER NOT NULL,
    nom VARCHAR(100) NOT NULL,
    loc_x FLOAT,
    loc_y FLOAT,
    loc_z FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_l) REFERENCES Logement(id)
);

CREATE TABLE Type_Capteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    unite_mesure VARCHAR(20),
    description TEXT
);

CREATE TABLE Capteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tc INTEGER NOT NULL,
    id_p INTEGER NOT NULL,
    ref_commerciale VARCHAR(100),
    precision_min FLOAT,
    precision_max FLOAT,
    port_comm VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tc) REFERENCES Type_Capteur(id),
    FOREIGN KEY (id_p) REFERENCES Piece(id)
);

CREATE TABLE Mesure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_c INTEGER NOT NULL,
    valeur FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_c) REFERENCES Capteur(id)
);

CREATE TABLE Type_Facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE Facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_l INTEGER NOT NULL,
    id_tc INTEGER NOT NULL,
    date_facture DATE NOT NULL,
    montant FLOAT,
    valeur_consommee FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_l) REFERENCES Logement(id),
    FOREIGN KEY (id_tc) REFERENCES Type_Facture(id)
);

-- Crée des index pour améliorer les performances
CREATE INDEX idx_piece_logement ON Piece(id_l);
CREATE INDEX idx_capteur_type ON Capteur(id_tc);
CREATE INDEX idx_capteur_piece ON Capteur(id_p);
CREATE INDEX idx_mesure_capteur ON Mesure(id_c);
CREATE INDEX idx_facture_logement ON Facture(id_l);
CREATE INDEX idx_facture_type ON Facture(id_tc);

-- Réactive les clés étrangères
PRAGMA foreign_keys = ON;