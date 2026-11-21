# Práctica Profesional 2 – Telco Customer Churn

Proyecto de limpieza, modelado relacional y consulta del dataset Telco Customer Churn (7.043 clientes, 21 variables).

## Contenido del repositorio

**/notebooks:** Notebook de Python (Google Colab) con el pipeline ETL comentado: exploración, limpieza e imputación del dataset. Genera `telco_limpio.csv`.

**/data_and_sql:** Base de datos MySQL.

- `DER_telco_churn_nuevo.png`: Diagrama Entidad-Relación diseñado en MySQL Workbench.
- `creacion_bd.sql`: crea la base de datos `telco`, la tabla plana de carga (`telco_limpio`) y las 4 tablas normalizadas en 3FN (`clientes`, `servicios`, `facturacion`, `registro_churn`), y las carga con INSERT ... SELECT.
- `consultas_churn.sql`: consultas de la actividad práctica (proyección con alias, WHERE, AND/OR, LIKE, ORDER BY y LIMIT).
- `clase4_dml_transacciones.sql`: INSERT, UPDATE con ROLLBACK y DELETE seguro dentro de transacciones.

## Flujo de trabajo

En Colab se ejecuta el notebook y se descarga `telco_limpio.csv`. En MySQL Workbench se importa el CSV a `telco_limpio` y se ejecuta `creacion_bd.sql`. Luego se ejecutan `consultas_churn.sql` y `clase4_dml_transacciones.sql` para analizar los datos.

## Modelo de datos

El dataset plano se separa en 4 entidades, todas relacionadas 1:1 con `clientes` mediante `id_cliente`:

| Tabla | PK | FK | Contenido |
|---|---|---|---|
| `clientes` | id_cliente | – | género, adulto mayor, pareja, dependientes, antigüedad |
| `servicios` | id_servicio | id_cliente | teléfono, internet y servicios adicionales |
| `facturacion` | id_factura | id_cliente | tipo de contrato, método de pago, cargo mensual y total |
| `registro_churn` | id_churn | id_cliente | indicador de churn |

**Del CSV plano a tablas separadas (3FN):** cada tabla agrupa atributos de una misma temática y todos dependen solo de su clave primaria. Esto elimina la redundancia (por ejemplo, las categorías duplicadas como "No internet service"), previene inconsistencias gracias a las claves foráneas y los tipos de datos, y optimiza las consultas, porque las tablas son más angostas y los JOIN se resuelven sobre claves indexadas.

## Consulta clave: churn y facturación por tipo de contrato

```sql
SELECT
    f.tipo_contrato                AS tipo_contrato,
    COUNT(*)                       AS cantidad_clientes,
    ROUND(AVG(f.cargo_mensual), 2) AS cargo_mensual_promedio,
    ROUND(AVG(rc.churn) * 100, 1)  AS porcentaje_churn
FROM facturacion AS f
JOIN registro_churn AS rc ON rc.id_cliente = f.id_cliente
GROUP BY f.tipo_contrato
ORDER BY porcentaje_churn DESC;
```

| Tipo de contrato | Clientes | Cargo mensual promedio | % churn |
|---|---|---|---|
| Month-to-month | 3.875 | 66,40 | 42,7 |
| One year | 1.473 | 65,05 | 11,3 |
| Two year | 1.695 | 60,77 | 2,8 |

Los clientes con contrato mensual abandonan unas 15 veces más que los de contrato a dos años y además pagan un cargo mensual más alto: fidelizar con contratos largos es una vía clara para reducir el churn.

## Hallazgos Visuales & Análisis Financiero

### Gráfico 1: Tasa de churn por tipo de contrato

![Churn por tipo de contrato](images/churn_por_contrato.png)

Los clientes con contrato **mes a mes (Month-to-month)** se dan de baja en un 42,7 % de los casos, contra 11,3 % en los contratos de un año y 2,8 % en los de dos años. Al no tener un compromiso de permanencia, el cliente puede irse apenas encuentra una mejor oferta. Por eso conviene impulsar campañas para que pasen a planes de largo plazo.

### Gráfico 2: Distribución de antigüedad (KDE)

![Densidad de antigüedad](images/densidad_antiguedad.png)

La curva roja (clientes que se fueron) se concentra en los primeros meses, mientras que la verde (clientes activos) crece hacia los 60–72 meses. El 55,5 % de las bajas ocurre en los **primeros 12 meses**, que es la ventana crítica. Ahí conviene reforzar el seguimiento y la fidelización del cliente nuevo.

### Gráfico 3: Matriz de impacto financiero

![Matriz de decisión financiera](images/matriz_decision_financiera.png)

La matriz asigna un valor en dólares a cada decisión: retener con éxito a un cliente que se iba suma $280 (verdadero positivo), una promoción innecesaria cuesta $50 (falso positivo), operar normal con un cliente estable cuesta $0 (verdadero negativo) y no detectar a un cliente que se va resta $600 (falso negativo). Un **falso negativo cuesta 12 veces más que un falso positivo**: si no detectáramos a ninguno de los 1.869 clientes que se fueron, la pérdida sería de unos $1.121.400. Por eso conviene aceptar algunas promociones de más antes que dejar escapar clientes en riesgo.


## Arquitectura de Datos

**Transacciones (COMMIT / ROLLBACK):** una transacción agrupa varias sentencias SQL en una unidad que se ejecuta completa o no se ejecuta. `START TRANSACTION` la inicia, `COMMIT` confirma los cambios y `ROLLBACK` los revierte. Se usaron para dar de alta un cliente completo sin dejar registros a medias, para simular un aumento del 10 % en los contratos mensuales que luego se canceló (el cargo promedio volvió de 73,05 a 66,40) y para validar un DELETE antes de hacerlo definitivo. Así se protege el dataset ante errores y los cambios son atómicos.

**Integridad referencial (FOREIGN KEY):** las claves foráneas aseguran que cada registro de `servicios`, `facturacion` y `registro_churn` pertenezca a un cliente existente. No permiten cargar datos de un cliente inexistente ni borrar un cliente que aún tiene registros asociados (error 1451), lo que evita datos huérfanos y mantiene la consistencia del dataset.
