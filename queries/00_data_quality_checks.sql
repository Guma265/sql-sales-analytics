-- 1) Duplicados potenciales en clientes (por nombre+ciudad)
SELECT nombre, ciudad, COUNT(*) AS total
FROM clientes
GROUP BY nombre, ciudad
HAVING COUNT(*) > 1;

-- 2) Precios inválidos (deberían ser > 0)
SELECT *
FROM productos
WHERE precio IS NULL OR precio <= 0;

-- 3) Ventas con cliente inexistente (huérfanos)
SELECT v.*
FROM ventas v
LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
WHERE c.id_cliente IS NULL;

-- 4) Ventas con producto inexistente (huérfanos)
SELECT v.*
FROM ventas v
LEFT JOIN productos p ON v.id_producto = p.id_producto
WHERE p.id_producto IS NULL;

