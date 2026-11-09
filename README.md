Proyecto de limpieza, modelado relacional y consulta del dataset Telco Customer Churn (7.043 clientes, 21 variables).

El repositorio contiene:
/notebooks	Notebook de Python (Google Colab) con el pipeline ETL comentado: exploración, limpieza e imputación del dataset. Genera telco_limpio.csv.
/data_and_sql	Base de datos MySQL: DER, script de creación y consultas.

Carpeta /data_and_sql
DER_telco: Diagrama Entidad-Relación diseñado en MySQL Workbench.
creacion_bd: crea la base de datos telco, la tabla plana de carga (telco_limpio), las 9 tablas normalizadas en 3FN (clientes, contratos, contrato_servicios, servicios, facturacion, registro_churn, tipos_contrato, tipos_internet, metodos_pago) y las carga con INSERT ... SELECT.
consultas_churn_sql: consultas de la actividad práctica (proyección con alias, WHERE, AND/OR, LIKE, ORDER BY y LIMIT).

Flujo de trabajo
En Colab se ejecuta el notebook y se descarga telco_limpio.csv.
En MySQL Workbench se importa el CSV a telco_limpio y se ejecuta creacion_bd.
Se ejecuta consultas_churn.sql para analizar los datos.
