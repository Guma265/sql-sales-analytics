# SQL Sales Analytics (SQLite)

Mini proyecto para practicar SQL con un caso de ventas usando SQLite.

## Dataset
Tablas:
- clientes(id_cliente, nombre, ciudad)
- productos(id_producto, nombre, precio)
- ventas(id_venta, id_cliente, id_producto, fecha)

## Cómo correr
1) Ejecuta `schema/01_create_tables.sql`
2) Ejecuta `data/02_insert_sample_data.sql`
3) Ejecuta queries en `queries/`

## Qué muestra este proyecto
- Joins y agregaciones
- Métricas por cliente/producto
- Series de tiempo por mes
- Top-N por grupo usando window functions

## Queries destacadas
- `queries/04_time_series.sql`: ventas e ingresos por mes
- `queries/02_customer_metrics.sql`: gasto por cliente + ranking
- `queries/03_product_metrics.sql`: ingresos por producto + productos sin ventas
- `queries/00_data_quality_checks.sql`: auditoría básica de calidad de datos

## Notas
- SQLite se usa para mantener el proyecto simple y reproducible.
- Las consultas usan buenas prácticas: alias claros, GROUP BY con IDs y window functions.
