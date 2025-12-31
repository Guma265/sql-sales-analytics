-- Ventas por mes
SELECT
  strftime('%Y-%m', v.fecha) AS mes,
  COUNT(*) AS total_ventas
FROM ventas v
GROUP BY mes
ORDER BY mes;

-- Ingresos por mes
SELECT
  strftime('%Y-%m', v.fecha) AS mes,
  SUM(p.precio) AS ingresos
FROM ventas v
JOIN productos p
  ON v.id_producto = p.id_producto
GROUP BY mes
ORDER BY mes;