-- GENERAL --

PRAGMA foreign_keys = ON;

-- Table grupo_usuario
DROP TABLE IF EXISTS grupo_usuario;
CREATE TABLE IF NOT EXISTS grupo_usuario (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL);

-- Table usuario
DROP TABLE IF EXISTS usuario;
CREATE TABLE IF NOT EXISTS usuario (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  id_grupo INTEGER NOT NULL,
  FOREIGN KEY (id_grupo) REFERENCES grupo_usuario (id));

-- Table auditor
DROP TABLE IF EXISTS auditor;
CREATE TABLE IF NOT EXISTS auditor (
  id INTEGER PRIMARY KEY,
  rut TEXT NOT NULL,
  nombre TEXT NOT NULL);

-- BUSES --

-- Table bus
DROP TABLE IF EXISTS bus;
CREATE TABLE IF NOT EXISTS bus (
  id INTEGER PRIMARY KEY,
  n_interno TEXT NOT NULL,
  patente TEXT NOT NULL,
  anio INTEGER NOT NULL,
  chasis TEXT NOT NULL,
  plazas INTEGER NOT NULL);

-- AUDITORIAS --

-- Table tipo_auditoria
DROP TABLE IF EXISTS tipo_auditoria;
CREATE TABLE IF NOT EXISTS tipo_auditoria (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL);

-- Table grupo_campos
DROP TABLE IF EXISTS grupo_campos;
CREATE TABLE IF NOT EXISTS grupo_campos (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL);

-- Table auditoria
DROP TABLE IF EXISTS auditoria;
CREATE TABLE IF NOT EXISTS auditoria (
  id INTEGER PRIMARY KEY,
  marca_temporal TIMESTAMP NOT NULL,
  fecha TIMESTAMP NOT NULL,
  id_grupo_campos INTEGER NOT NULL,
  id_bus INTEGER NOT NULL,
  id_tipo_auditoria INTEGER NOT NULL,
  id_auditor INTEGER NOT NULL,
  FOREIGN KEY (id_grupo_campos) REFERENCES grupo_campos (id),
  FOREIGN KEY (id_bus) REFERENCES bus (id),
  FOREIGN KEY (id_tipo_auditoria) REFERENCES tipo_auditoria (id),
  FOREIGN KEY (id_auditor) REFERENCES auditor (id));

-- Table campo_auditoria
DROP TABLE IF EXISTS campo_auditoria;
CREATE TABLE IF NOT EXISTS campo_auditoria (
  id INTEGER PRIMARY KEY,
  id_grupo INTEGER NOT NULL,
  titulo TEXT NOT NULL,
  FOREIGN KEY (id_grupo) REFERENCES grupo_campos (id));

-- Table respuesta_auditoria
DROP TABLE IF EXISTS respuesta_auditoria;
CREATE TABLE IF NOT EXISTS respuesta_auditoria (
  id_auditoria INTEGER NOT NULL,
  id_campo_auditoria INTEGER NOT NULL,
  valor TEXT NOT NULL,
  UNIQUE (id_auditoria, id_campo_auditoria),
  PRIMARY KEY (id_auditoria, id_campo_auditoria),
  FOREIGN KEY (id_auditoria) REFERENCES auditoria (id),
  FOREIGN KEY (id_campo_auditoria) REFERENCES campo_auditoria (id));


INSERT INTO grupo_usuario VALUES(1, 'Auditoria');
INSERT INTO grupo_usuario VALUES(2, 'Digitador');
INSERT INTO grupo_usuario VALUES(3, 'Administrador');

INSERT INTO usuario VALUES('auditor', 'test', 1);
INSERT INTO usuario VALUES('digitador', 'test', 2);
INSERT INTO usuario VALUES('administrador', 'test', 3);