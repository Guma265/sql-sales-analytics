-- Top 1 producto más vendido por cliente
WITH ventas_por_cliente_producto AS (
    SELECT
        c.id_cliente,
        c.nombre AS cliente,
        p.id_producto,
        p.nombre AS producto,
        COUNT(v.id_venta) AS total_ventas
    FROM ventas v
    JOIN clientes c ON v.id_cliente = c.id_cliente
    JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY c.id_cliente, c.nombre, p.id_producto, p.nombre
),
ranking AS (
    SELECT
        id_cliente, cliente, id_producto, producto, total_ventas,
        DENSE_RANK() OVER (
            PARTITION BY id_cliente
            ORDER BY total_ventas DESC
        ) AS rnk
    FROM ventas_por_cliente_producto
)
SELECT id_cliente, cliente, id_producto, producto, total_ventas
FROM ranking
WHERE rnk = 1
ORDER BY id_cliente;
