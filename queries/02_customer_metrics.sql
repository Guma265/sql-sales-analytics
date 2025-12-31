-- Gasto total por cliente
SELECT
  c.id_cliente,
  c.nombre AS cliente,
  COALESCE(SUM(p.precio), 0) AS gasto_total
FROM clientes c
LEFT JOIN ventas v
  ON c.id_cliente = v.id_cliente
LEFT JOIN productos p
  ON v.id_producto = p.id_producto
GROUP BY c.id_cliente, c.nombre
ORDER BY gasto_total DESC;

-- Ranking de clientes por gasto
WITH gasto_por_cliente AS (
  SELECT
    c.id_cliente,
    c.nombre AS cliente,
    COALESCE(SUM(p.precio), 0) AS gasto_total
  FROM clientes c
  LEFT JOIN ventas v ON c.id_cliente = v.id_cliente
  LEFT JOIN productos p ON v.id_producto = p.id_producto
  GROUP BY c.id_cliente, c.nombre
)
SELECT
  id_cliente,
  cliente,
  gasto_total,
  DENSE_RANK() OVER (ORDER BY gasto_total DESC) AS ranking
FROM gasto_por_cliente
ORDER BY ranking, id_cliente;
