-- GENERAL --

PRAGMA foreign_keys = ON;

-- Table app_user
DROP TABLE IF EXISTS app_user;
CREATE TABLE IF NOT EXISTS app_user (
  user_name TEXT PRIMARY KEY,
  password TEXT NOT NULL);

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
  nombre TEXT NOT NULL,
  responsable INTEGER DEFAULT 0);

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