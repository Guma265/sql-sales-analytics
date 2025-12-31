-- Ingresos por producto
SELECT
  p.id_producto,
  p.nombre AS producto,
  COUNT(v.id_venta) AS veces_vendido,
  COALESCE(SUM(p.precio), 0) AS ingresos
FROM productos p
LEFT JOIN ventas v
  ON p.id_producto = v.id_producto
GROUP BY p.id_producto, p.nombre
ORDER BY ingresos DESC;

-- Productos que nunca se vendieron
SELECT
  p.id_producto,
  p.nombre,
  p.precio
FROM productos p
LEFT JOIN ventas v
  ON p.id_producto = v.id_producto
WHERE v.id_producto IS NULL
ORDER BY p.id_producto;
