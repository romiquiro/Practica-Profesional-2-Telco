CREATE DATABASE telco;
USE telco;

-- Importar con: clic derecho > Table Data Import Wizard > telco_limpio.csv
CREATE telco_limpio (
    id_cliente             VARCHAR(10),
    genero                 VARCHAR(10),
    adulto_mayor           TINYINT,
    tiene_pareja           TINYINT,
    tiene_dependientes     TINYINT,
    antiguedad_meses       INT,
    servicio_telefonico    TINYINT,
    lineas_multiples       TINYINT,
    tipo_internet          VARCHAR(30),
    seguridad_online       TINYINT,
    respaldo_online        TINYINT,
    proteccion_dispositivo TINYINT,
    soporte_tecnico        TINYINT,
    streaming_tv           TINYINT,
    streaming_peliculas    TINYINT,
    tipo_contrato          VARCHAR(30),
    factura_electronica    TINYINT,
    metodo_pago            VARCHAR(40),
    cargo_mensual          DECIMAL(8,2),
    cargo_total            DECIMAL(10,2),
    churn                  TINYINT
);
 
-- ---------- Catalogos ----------
CREATE TABLE tipos_contrato (
    id_tipo_contrato INT NOT NULL AUTO_INCREMENT,
    nombre           VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (id_tipo_contrato)
);
CREATE TABLE tipos_internet (
    id_tipo_internet INT NOT NULL AUTO_INCREMENT,
    nombre           VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (id_tipo_internet)
);
CREATE TABLE metodos_pago (
    id_metodo_pago INT NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(40) NOT NULL UNIQUE,
    PRIMARY KEY (id_metodo_pago)
);
CREATE TABLE servicios (
    id_servicio INT NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(40) NOT NULL UNIQUE,
    PRIMARY KEY (id_servicio)
);
 
-- ---------- Entidades principales ----------
CREATE TABLE clientes (
    id_cliente         VARCHAR(10) NOT NULL,
    genero             VARCHAR(10) NOT NULL,
    adulto_mayor       TINYINT NOT NULL,
    tiene_pareja       TINYINT NOT NULL,
    tiene_dependientes TINYINT NOT NULL,
    PRIMARY KEY (id_cliente)
);
CREATE TABLE contratos (
    id_contrato      INT NOT NULL AUTO_INCREMENT,
    id_cliente       VARCHAR(10) NOT NULL UNIQUE,   -- relacion 1:1 con clientes
    id_tipo_contrato INT NOT NULL,
    id_tipo_internet INT NOT NULL,
    antiguedad_meses INT NOT NULL,
    PRIMARY KEY (id_contrato),
    FOREIGN KEY (id_cliente)       REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_tipo_contrato) REFERENCES tipos_contrato(id_tipo_contrato),
    FOREIGN KEY (id_tipo_internet) REFERENCES tipos_internet(id_tipo_internet)
);
CREATE TABLE contrato_servicios (                    -- relacion N:M
    id_contrato INT NOT NULL,
    id_servicio INT NOT NULL,
    PRIMARY KEY (id_contrato, id_servicio),
    FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
);
CREATE TABLE facturacion (
    id_contrato         INT NOT NULL,
    id_metodo_pago      INT NOT NULL,
    factura_electronica TINYINT NOT NULL,
    cargo_mensual       DECIMAL(8,2)  NOT NULL,
    cargo_total         DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_contrato),
    FOREIGN KEY (id_contrato)    REFERENCES contratos(id_contrato),
    FOREIGN KEY (id_metodo_pago) REFERENCES metodos_pago(id_metodo_pago)
);
CREATE TABLE registro_churn (
    id_contrato INT NOT NULL,
    churn       TINYINT NOT NULL,
    PRIMARY KEY (id_contrato),
    FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato)
);
 
-- ---------- Carga desde la tabla plana ----------
INSERT INTO tipos_contrato (nombre) SELECT DISTINCT tipo_contrato FROM telco_limpio;
INSERT INTO tipos_internet (nombre) SELECT DISTINCT tipo_internet FROM telco_limpio;
INSERT INTO metodos_pago   (nombre) SELECT DISTINCT metodo_pago   FROM telco_limpio;
INSERT INTO servicios (nombre) VALUES
 ('servicio_telefonico'), ('lineas_multiples'), ('seguridad_online'),
 ('respaldo_online'), ('proteccion_dispositivo'), ('soporte_tecnico'),
 ('streaming_tv'), ('streaming_peliculas');
 
INSERT INTO clientes (id_cliente, genero, adulto_mayor, tiene_pareja, tiene_dependientes)
SELECT id_cliente, genero, adulto_mayor, tiene_pareja, tiene_dependientes FROM telco_limpio;
 
INSERT INTO contratos (id_cliente, id_tipo_contrato, id_tipo_internet, antiguedad_meses)
SELECT t.id_cliente, tc.id_tipo_contrato, ti.id_tipo_internet, t.antiguedad_meses
FROM telco_limpio t
JOIN tipos_contrato tc ON tc.nombre = t.tipo_contrato
JOIN tipos_internet ti ON ti.nombre = t.tipo_internet;
 
INSERT INTO contrato_servicios (id_contrato, id_servicio)
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'servicio_telefonico'    WHERE t.servicio_telefonico = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'lineas_multiples'       WHERE t.lineas_multiples = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'seguridad_online'       WHERE t.seguridad_online = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'respaldo_online'        WHERE t.respaldo_online = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'proteccion_dispositivo' WHERE t.proteccion_dispositivo = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'soporte_tecnico'        WHERE t.soporte_tecnico = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'streaming_tv'           WHERE t.streaming_tv = 1
UNION ALL
SELECT c.id_contrato, s.id_servicio FROM telco_limpio t JOIN contratos c ON c.id_cliente = t.id_cliente JOIN servicios s ON s.nombre = 'streaming_peliculas'    WHERE t.streaming_peliculas = 1;
 
INSERT INTO facturacion (id_contrato, id_metodo_pago, factura_electronica, cargo_mensual, cargo_total)
SELECT c.id_contrato, mp.id_metodo_pago, t.factura_electronica, t.cargo_mensual, t.cargo_total
FROM telco_limpio t
JOIN contratos c     ON c.id_cliente = t.id_cliente
JOIN metodos_pago mp ON mp.nombre = t.metodo_pago;
 
INSERT INTO registro_churn (id_contrato, churn)
SELECT c.id_contrato, t.churn
FROM telco_limpio t
JOIN contratos c ON c.id_cliente = t.id_cliente;
