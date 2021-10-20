## Script de création de la base de données pour le projet de session.
CREATE TABLE "declarations" (
	"NO_DECLARATION"	INTEGER NOT NULL,
	"DATE_DECLARATION"	TEXT NOT NULL,
	"DATE_INSP_VISPRE"	TEXT NOT NULL,
	"NBR_EXTERMIN"	TEXT,
	"DATE_DEBUTTRAIT"	TEXT,
	"DATE_FINTRAIT"	TEXT,
	"No_QR"	TEXT NOT NULL,
	"NOM_QR"	TEXT NOT NULL,
	"NOM_ARROND"	TEXT NOT NULL,
	"COORD_X"	NUMERIC NOT NULL,
	"COORD_Y"	REAL NOT NULL,
	"LONGITUDE"	NUMERIC NOT NULL,
	"LATITUDE"	NUMERIC NOT NULL,
	PRIMARY KEY("NO_DECLARATION")
);

CREATE TABLE "users" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"fullname"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"liste_quartiers"	TEXT,
	"picture"	BLOB,
	"salt"	TEXT NOT NULL,
	"hash"	TEXT NOT NULL
);

CREATE TABLE "sessions" (
	"id"	integer,
	"id_session"	varchar(32),
	"email"	varchar(25),
	PRIMARY KEY("id")
);

create table "pictures" (
  id varchar(32) primary key,
  data blob
);