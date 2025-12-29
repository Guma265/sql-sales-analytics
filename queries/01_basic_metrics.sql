-- Total ventas
SELECT COUNT(*) AS total_ventas
FROM ventas;

-- Ingresos totales
SELECT SUM(p.precio) AS ingresos_totales
FROM ventas v
JOIN productos p ON v.id_producto = p.id_producto;
