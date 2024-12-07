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
  FOREIGN KEY (id_grupo) REFERENCES grupo_campos (id) ON DELETE CASCADE);

-- Table respuesta_auditoria
DROP TABLE IF EXISTS respuesta_auditoria;
CREATE TABLE IF NOT EXISTS respuesta_auditoria (
  id_auditoria INTEGER NOT NULL,
  id_campo_auditoria INTEGER NOT NULL,
  valor TEXT NOT NULL,
  UNIQUE (id_auditoria, id_campo_auditoria),
  PRIMARY KEY (id_auditoria, id_campo_auditoria),
  FOREIGN KEY (id_auditoria) REFERENCES auditoria (id) ON DELETE CASCADE,
  FOREIGN KEY (id_campo_auditoria) REFERENCES campo_auditoria (id) ON DELETE CASCADE);


INSERT INTO grupo_usuario VALUES(1, 'Auditoria');
INSERT INTO grupo_usuario VALUES(2, 'Digitador');
INSERT INTO grupo_usuario VALUES(3, 'Administrador');

INSERT INTO usuario VALUES('auditor', 'test', 1);
INSERT INTO usuario VALUES('digitador', 'test', 2);
INSERT INTO usuario VALUES('administrador', 'test', 3);

INSERT INTO auditor(rut, nombre) VALUES('11.111.111-1', 'Auditor1');
INSERT INTO auditor(rut, nombre) VALUES('22.222.222-2', 'Auditor2');

INSERT INTO tipo_auditoria(nombre) VALUES('Seguimiento');
INSERT INTO tipo_auditoria(nombre) VALUES('No auditable');

INSERT INTO bus (n_interno, patente, anio, chasis, plazas)
VALUES ('B-001', 'ABC-123', 2020, 'CHS-0001', 50);
INSERT INTO bus (n_interno, patente, anio, chasis, plazas)
VALUES ('B-002', 'ABC-321', 2021, 'CHS-0001', 50);
INSERT INTO bus (n_interno, patente, anio, chasis, plazas)
VALUES ('B-003', 'ABC-333', 2021, 'CHS-0002', 50);

INSERT INTO grupo_campos(nombre) VALUES('Torniquete');
INSERT INTO grupo_campos(nombre) VALUES('Ruteros');

INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(1, 'Funcionamiento');
INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(1, 'Limpieza');
INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(1, 'Tipo');

INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(2, 'Funcionamiento R1');
INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(2, 'Limpieza R1');
INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(2, 'Funcionamiento R2');
INSERT INTO campo_auditoria(id_grupo, titulo) VALUES(2, 'Limpieza R2');

INSERT INTO auditoria(marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor)
VALUES (CURRENT_TIMESTAMP, '2024-12-06 2:00:00', 1, 1, 1, 1);
INSERT INTO auditoria(marca_temporal, fecha, id_grupo_campos, id_bus, id_tipo_auditoria, id_auditor)
VALUES (CURRENT_TIMESTAMP, '2024-12-07 3:00:00', 2, 2, 2, 2);

INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(1, 1, 'Funciona');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(1, 2, 'Limpio');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(1, 3, '3 Brazos');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(2, 4, 'Funciona');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(2, 5, 'Sucio');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(2, 6, 'No Funciona');
INSERT INTO respuesta_auditoria(id_auditoria, id_campo_auditoria, valor) VALUES(2, 7, 'Muy Sucio');