-- CLASE 4: INSERT, UPDATE + ROLLBACK/COMMIT y DELETE seguro
-- Base de datos: telco (4 entidades: clientes, servicios, facturacion, registro_churn)
-- =====================================================================
-- Equivalencias: pareja 'Yes' -> tiene_pareja = 1 | dependientes 'No' -> tiene_dependientes = 0
-- Supuestos para campos obligatorios que el enunciado no indica:
--   antiguedad_meses = 1, internet 'Fiber optic', pago 'Electronic check',
--   factura electronica = 1, servicios: telefono y seguridad online.
-- =====================================================================
USE telco;

-- =====================================================================
-- PARTE 1: ALTA DE NUEVOS REGISTROS (INSERT)

START TRANSACTION;

-- 1.1) Nuevo cliente (tabla padre: se inserta primero por la FOREIGN KEY)
INSERT INTO clientes (id_cliente, genero, adulto_mayor, tiene_pareja, tiene_dependientes, antiguedad_meses)
VALUES ('9999-NEWCL', 'Female', 0, 1, 0, 1);

-- 1.2) Servicios: id_servicio NO se especifica porque es AUTO_INCREMENT
INSERT INTO servicios (id_cliente, servicio_telefonico, lineas_multiples, tipo_internet,
                       seguridad_online, respaldo_online, proteccion_dispositivo,
                       soporte_tecnico, streaming_tv, streaming_peliculas)
VALUES ('9999-NEWCL', 1, 0, 'Fiber optic', 1, 0, 0, 0, 0, 0);

-- 1.3) Facturacion (id_factura tambien es AUTO_INCREMENT)
INSERT INTO facturacion (id_cliente, tipo_contrato, factura_electronica, metodo_pago,
                         cargo_mensual, cargo_total)
VALUES ('9999-NEWCL', 'Month-to-month', 1, 'Electronic check', 85.50, 85.50);

-- 1.4) Registro de churn inicial (0 = cliente activo)
INSERT INTO registro_churn (id_cliente, churn)
VALUES ('9999-NEWCL', 0);

COMMIT;

-- 1.5) Verificacion del alta
SELECT
    c.id_cliente,
    c.genero,
    c.tiene_pareja,
    s.id_servicio,
    s.tipo_internet,
    f.tipo_contrato,
    f.cargo_mensual,
    f.cargo_total,
    rc.churn
FROM clientes AS c
JOIN servicios       AS s  ON s.id_cliente  = c.id_cliente
JOIN facturacion     AS f  ON f.id_cliente  = c.id_cliente
JOIN registro_churn  AS rc ON rc.id_cliente = c.id_cliente
WHERE c.id_cliente = '9999-NEWCL';

-- =====================================================================
-- PARTE 2: REAJUSTE TARIFARIO CON ROLLBACK (UPDATE)
-- =====================================================================

SET SQL_SAFE_UPDATES = 0;

-- 2.1) Estado ORIGINAL
SELECT
    COUNT(*)                       AS clientes_mes_a_mes,
    ROUND(AVG(f.cargo_mensual), 2) AS cargo_promedio_original,
    ROUND(SUM(f.cargo_mensual), 2) AS cargo_total_original
FROM facturacion AS f
WHERE f.tipo_contrato = 'Month-to-month';

-- 2.2) Transaccion explicita
START TRANSACTION;

-- 2.3) Aumento del 10% solo para contratos mes a mes
UPDATE facturacion
SET cargo_mensual = ROUND(cargo_mensual * 1.10, 2)
WHERE tipo_contrato = 'Month-to-month';

-- 2.4) Comprobar los nuevos montos (dentro de la transaccion)
SELECT
    COUNT(*)                       AS clientes_mes_a_mes,
    ROUND(AVG(f.cargo_mensual), 2) AS cargo_promedio_con_aumento,
    ROUND(SUM(f.cargo_mensual), 2) AS cargo_total_con_aumento
FROM facturacion AS f
WHERE f.tipo_contrato = 'Month-to-month';

SELECT f.id_cliente, f.cargo_mensual            -- el cliente nuevo pasa de 85.50 a 94.05
FROM facturacion AS f
WHERE f.id_cliente = '9999-NEWCL';

-- 2.5) El area comercial cancela el aumento -> ROLLBACK
ROLLBACK;

-- 2.6) Verificar que los valores volvieron al estado original
SELECT
    COUNT(*)                       AS clientes_mes_a_mes,
    ROUND(AVG(f.cargo_mensual), 2) AS cargo_promedio_restaurado,
    ROUND(SUM(f.cargo_mensual), 2) AS cargo_total_restaurado
FROM facturacion AS f
WHERE f.tipo_contrato = 'Month-to-month';

SELECT f.id_cliente, f.cargo_mensual            -- vuelve a 85.50
FROM facturacion AS f
WHERE f.id_cliente = '9999-NEWCL';

-- =====================================================================
-- PARTE 3: ELIMINACION SEGURA (DELETE)
-- Purga de registros de churn de clientes inactivos (churn = 1) especificos
-- =====================================================================
START TRANSACTION;

-- 3.1) PRIMERO validar con SELECT que filas se van a borrar (deben ser 3)
SELECT rc.id_churn, rc.id_cliente, rc.churn
FROM registro_churn AS rc
WHERE rc.id_cliente IN ('0023-HGHWL', '0032-PGELS', '0107-WESLM')
  AND rc.churn = 1;

SELECT COUNT(*) AS registros_churn_antes FROM registro_churn;

-- 3.2) DELETE con la MISMA condicion validada arriba
DELETE FROM registro_churn
WHERE id_cliente IN ('0023-HGHWL', '0032-PGELS', '0107-WESLM')
  AND churn = 1;

-- 3.3) Comprobar el efecto dentro de la transaccion
SELECT COUNT(*) AS registros_churn_despues FROM registro_churn;   -- 3 menos

-- 3.4) Por seguridad se deshace el borrado.
-- Si la purga debe ser definitiva, reemplazar ROLLBACK por COMMIT.
ROLLBACK;

-- 3.5) Verificar que los datos siguen intactos
SELECT COUNT(*) AS registros_churn_final FROM registro_churn;



SET SQL_SAFE_UPDATES = 1;
