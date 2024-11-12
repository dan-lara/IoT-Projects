CREATE TABLE "Ville" (
  "code" integer,
  "nom" text
);

CREATE TABLE "Adresse" (
  "id" integer PRIMARY KEY,
  "numero" integer,
  "voie" text,
  "nom_voie" text,
  "code" integer
);

CREATE TABLE "Logement" (
  "id" integer PRIMARY KEY,
  "id_adresse" integer,
  "numero_telephone" varchar,
  "adresse_ip" ip,
  "created_at" timestamp
);

CREATE TABLE "Piece" (
  "id" integer PRIMARY KEY,
  "id_l" integer,
  "nom" varchar,
  "loc" float[3],
  "created_at" timestamp
);

CREATE TABLE "Type_Capteur" (
  "id" integer PRIMARY KEY,
  "nom" varchar,
  "unite_mesure" varchar(20),
  "description" text
);

CREATE TABLE "Capteur" (
  "id" integer PRIMARY KEY,
  "id_tc" integer,
  "id_p" integer,
  "ref_commerciale" varchar,
  "precision_min" float(10,2),
  "precision_max" float(10,2),
  "port_comm" varchar,
  "created_at" timestamp
);

CREATE TABLE "Mesure" (
  "id" integer PRIMARY KEY,
  "id_c" integer,
  "valeur" float(10,2),
  "created_at" timestamp
);

CREATE TABLE "Type_Facture" (
  "id" integer PRIMARY KEY,
  "nom" varchar,
  "description" text
);

CREATE TABLE "Facture" (
  "id" integer PRIMARY KEY,
  "id_l" integer,
  "id_tc" integer,
  "date_facture" date,
  "montant" float(10,2),
  "valeur_consommee" float(10,2),
  "created_at" timestamp
);

ALTER TABLE "Adresse" ADD FOREIGN KEY ("code") REFERENCES "Ville" ("code");

ALTER TABLE "Logement" ADD FOREIGN KEY ("id_adresse") REFERENCES "Adresse" ("id");

ALTER TABLE "Piece" ADD FOREIGN KEY ("id_l") REFERENCES "Logement" ("id");

ALTER TABLE "Capteur" ADD FOREIGN KEY ("id_tc") REFERENCES "Type_Capteur" ("id");

ALTER TABLE "Capteur" ADD FOREIGN KEY ("id_p") REFERENCES "Piece" ("id");

ALTER TABLE "Mesure" ADD FOREIGN KEY ("id_c") REFERENCES "Capteur" ("id");

ALTER TABLE "Facture" ADD FOREIGN KEY ("id_l") REFERENCES "Logement" ("id");

ALTER TABLE "Facture" ADD FOREIGN KEY ("id_tc") REFERENCES "Type_Facture" ("id");
