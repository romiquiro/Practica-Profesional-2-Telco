-- CONSULTAS CHURN - Ejercicios 1 a 5
-- Base de datos: telco (4 entidades: clientes, servicios, facturacion, registro_churn)
-- =====================================================================
USE telco;

-- ---------------------------------------------------------------------
-- EJERCICIO 1: Proyeccion (SELECT y FROM) con alias (AS)
-- ---------------------------------------------------------------------
SELECT
    c.id_cliente   AS cliente_id,
    c.genero       AS genero_cliente,
    c.adulto_mayor AS es_adulto_mayor
FROM clientes AS c;

-- ---------------------------------------------------------------------
-- EJERCICIO 2: Filtrado con operadores de comparacion (WHERE)
-- ---------------------------------------------------------------------
SELECT
    f.id_cliente     AS cliente_id,
    f.tipo_contrato  AS tipo_contrato,
    f.cargo_mensual  AS cargo_mensual
FROM facturacion AS f
WHERE f.cargo_mensual > 70.00;

-- ---------------------------------------------------------------------
-- EJERCICIO 3: Operadores logicos (AND, OR)
-- ---------------------------------------------------------------------
-- 3.1) Contrato 'Month-to-month' Y cargo mensual mayor a 50.00
SELECT
    f.id_cliente     AS cliente_id,
    f.tipo_contrato  AS tipo_contrato,
    f.cargo_mensual  AS cargo_mensual
FROM facturacion AS f
WHERE f.tipo_contrato = 'Month-to-month'
  AND f.cargo_mensual > 50.00;

-- 3.2) Se suman los clientes que pagan con 'Electronic check'
-- Los parentesis agrupan la primera condicion antes de aplicar el OR
SELECT
    f.id_cliente     AS cliente_id,
    f.tipo_contrato  AS tipo_contrato,
    f.metodo_pago    AS metodo_pago,
    f.cargo_mensual  AS cargo_mensual
FROM facturacion AS f
WHERE (f.tipo_contrato = 'Month-to-month' AND f.cargo_mensual > 50.00)
   OR f.metodo_pago = 'Electronic check';

-- ---------------------------------------------------------------------
-- EJERCICIO 4: Patrones de texto (LIKE) y ordenamiento (ORDER BY)
-- ---------------------------------------------------------------------
-- 4.1) Metodos de pago que contienen la palabra 'Electronic'
SELECT
    f.id_cliente     AS cliente_id,
    f.metodo_pago    AS metodo_pago,
    f.cargo_mensual  AS cargo_mensual
FROM facturacion AS f
WHERE f.metodo_pago LIKE '%Electronic%';

-- 4.2) Mismo resultado, ordenado por cargo mensual de mayor a menor
SELECT
    f.id_cliente     AS cliente_id,
    f.metodo_pago    AS metodo_pago,
    f.cargo_mensual  AS cargo_mensual
FROM facturacion AS f
WHERE f.metodo_pago LIKE '%Electronic%'
ORDER BY f.cargo_mensual DESC;

-- ---------------------------------------------------------------------
-- EJERCICIO 5: Limitacion de resultados (LIMIT)
-- Top 5 clientes con mayor cargo total acumulado
-- ---------------------------------------------------------------------
SELECT
    f.id_cliente   AS cliente_id,
    f.cargo_total  AS cargo_total_acumulado
FROM facturacion AS f
ORDER BY f.cargo_total DESC,
         f.id_cliente ASC          -- desempate para que el orden sea siempre el mismo
LIMIT 5;

-- ---------------------------------------------------------------------
-- CONSULTA CLAVE (analisis comercial): churn y cargo promedio por tipo de contrato
-- ---------------------------------------------------------------------
SELECT
    f.tipo_contrato                    AS tipo_contrato,
    COUNT(*)                           AS cantidad_clientes,
    ROUND(AVG(f.cargo_mensual), 2)     AS cargo_mensual_promedio,
    ROUND(AVG(rc.churn) * 100, 1)      AS porcentaje_churn
FROM facturacion AS f
JOIN registro_churn AS rc ON rc.id_cliente = f.id_cliente
GROUP BY f.tipo_contrato
ORDER BY porcentaje_churn DESC;
