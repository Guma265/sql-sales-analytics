INSERT INTO clientes (id_cliente, nombre, ciudad) VALUES
(1, 'Ana', 'CDMX'),
(2, 'Luis', 'Guadalajara'),
(3, 'Marta', 'Monterrey');

INSERT INTO productos (id_producto, nombre, precio) VALUES
(1, 'Laptop', 15000),
(2, 'Mouse', 500),
(3, 'Teclado', 900);

INSERT INTO ventas (id_venta, id_cliente, id_producto, fecha) VALUES
(1, 1, 1, '2024-01-10'),
(2, 1, 2, '2024-01-11'),
(3, 2, 2, '2024-01-12'),
(4, 2, 3, '2024-02-01'),
(5, 3, 2, '2024-02-05');
