-- -----------------------------------------------------
-- Schema Subus
-- -----------------------------------------------------

DROP SCHEMA Subus CASCADE;
CREATE SCHEMA IF NOT EXISTS Subus;
SET search_path TO Subus;


-- GENERAL --

-- -----------------------------------------------------
-- Table Subus.app_user
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.app_user;

CREATE TABLE IF NOT EXISTS Subus.app_user (
  user_name VARCHAR(128) PRIMARY KEY,
  password VARCHAR(64) NOT NULL);

-- -----------------------------------------------------
-- Table Subus.auditor
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.auditor;

CREATE TABLE IF NOT EXISTS Subus.auditor (
  id SERIAL NOT NULL,
  rut VARCHAR(15) NOT NULL,
  nombre VARCHAR(128) NOT NULL,
  PRIMARY KEY (id));


-- BUSES --

-- -----------------------------------------------------
-- Table Subus.bus
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.bus;

CREATE TABLE IF NOT EXISTS Subus.bus (
  id SERIAL PRIMARY KEY,
  n_interno VARCHAR(8) NOT NULL,
  patente VARCHAR(8) NOT NULL,
  anio SMALLINT NOT NULL,
  chasis VARCHAR(64) NOT NULL,
  plazas SMALLINT NOT NULL);


-- AUDITORIAS --

-- -----------------------------------------------------
-- Table Subus.tipo_auditoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.tipo_auditoria;

CREATE TABLE IF NOT EXISTS Subus.tipo_auditoria (
  id SERIAL NOT NULL ,
  nombre VARCHAR(64) NOT NULL,
  PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table Subus.grupo_campos
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.grupo_campos;

CREATE TABLE IF NOT EXISTS Subus.grupo_campos (
  id SERIAL NOT NULL ,
  nombre VARCHAR(64) NOT NULL,
  respondible BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table Subus.grupo_en_grupo
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.grupo_en_grupo;

CREATE TABLE IF NOT EXISTS Subus.grupo_en_grupo (
  id_grupo_padre INT NOT NULL,
  id_grupo_hijo INT NOT NULL,
  orden INT NOT NULL,
  UNIQUE (id_grupo_padre, orden),
  PRIMARY KEY (id_grupo_padre, id_grupo_hijo),
  CONSTRAINT grupo_en_grupo_ibfk_1
    FOREIGN KEY (id_grupo_padre)
    REFERENCES Subus.grupo_campos (id),
  CONSTRAINT grupo_en_grupo_ibfk_2
    FOREIGN KEY (id_grupo_hijo)
    REFERENCES Subus.grupo_campos (id));


-- -----------------------------------------------------
-- Table Subus.auditoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.auditoria;

CREATE TABLE IF NOT EXISTS Subus.auditoria (
  id SERIAL NOT NULL ,
  marca_temporal TIMESTAMP NOT NULL,
  fecha TIMESTAMP NOT NULL,
  id_grupo_campos INT NOT NULL,
  id_bus INT NOT NULL,
  id_tipo_auditoria INT NOT NULL,
  id_auditor INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT auditoria_ibfk_1
    FOREIGN KEY (id_grupo_campos)
    REFERENCES Subus.grupo_campos (id),
  CONSTRAINT auditoria_ibfk_2
    FOREIGN KEY (id_bus)
    REFERENCES Subus.bus (id),
  CONSTRAINT auditoria_ibfk_3
    FOREIGN KEY (id_patio)
    REFERENCES Subus.patio (id),
  CONSTRAINT auditoria_ibfk_4
    FOREIGN KEY (id_tipo_auditoria)
    REFERENCES Subus.tipo_auditoria (id),
  CONSTRAINT auditoria_ibfk_5
    FOREIGN KEY (id_auditor)
    REFERENCES Subus.auditor (id));


-- -----------------------------------------------------
-- Table Subus.campo_auditoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.campo_auditoria;

CREATE TABLE IF NOT EXISTS Subus.campo_auditoria (
  id SERIAL NOT NULL ,
  id_grupo INT NOT NULL,
  titulo VARCHAR(128) NOT NULL,
  tipo VARCHAR(64) NOT NULL DEFAULT 'Texto',
  descripcion VARCHAR(512),
  PRIMARY KEY (id),
  CONSTRAINT campo_auditoria_ibfk_1
    FOREIGN KEY (id_grupo)
    REFERENCES Subus.grupo_campos (id));


-- -----------------------------------------------------
-- Table Subus.campo_opcion
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.campo_opcion;

CREATE TABLE IF NOT EXISTS Subus.campo_opcion (
  id SERIAL NOT NULL,
  id_campo_auditoria INT NOT NULL,
  valor VARCHAR(128) NOT NULL,
  abreviacion VARCHAR(32),
  id_nivel_alerta INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT campo_opcion_ibfk_1
    FOREIGN KEY (id_campo_auditoria)
    REFERENCES Subus.campo_auditoria (id),
  CONSTRAINT campo_opcion_ibfk_2
    FOREIGN KEY (id_nivel_alerta)
    REFERENCES Subus.nivel_alerta (id));


-- -----------------------------------------------------
-- Table Subus.opcion_en_auditoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.opcion_en_auditoria;

CREATE TABLE IF NOT EXISTS Subus.opcion_en_auditoria (
  id_auditoria INT NOT NULL ,
  id_campo_opcion INT NOT NULL,
  orden INT NOT NULL,
  UNIQUE (id_auditoria, orden),
  PRIMARY KEY (id_auditoria, id_campo_opcion),
  CONSTRAINT opcion_en_auditoria_ibfk_1
    FOREIGN KEY (id_auditoria)
    REFERENCES Subus.auditoria (id),
  CONSTRAINT opcion_en_auditoria_ibfk_2
    FOREIGN KEY (id_campo_opcion)
    REFERENCES Subus.campo_opcion (id));


-- -----------------------------------------------------
-- Table Subus.texto_en_auditoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Subus.texto_en_auditoria;

CREATE TABLE IF NOT EXISTS Subus.texto_en_auditoria (
  id_auditoria INT NOT NULL,
  id_campo_auditoria INT NOT NULL,
  valor VARCHAR(512) NOT NULL,
  orden INT NOT NULL,
  UNIQUE (id_auditoria, orden),
  PRIMARY KEY (id_auditoria, id_campo_auditoria),
  CONSTRAINT texto_en_auditoria_ibfk_1
    FOREIGN KEY (id_auditoria)
    REFERENCES Subus.auditoria (id),
  CONSTRAINT texto_en_auditoria_ibfk_2
    FOREIGN KEY (id_campo_auditoria)
    REFERENCES Subus.campo_auditoria (id));
