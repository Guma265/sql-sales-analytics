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
