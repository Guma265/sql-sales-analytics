import sqlite3
import pandas as pd
from pathlib import Path

# 1) Paths reales en tu máquina
sql_dir = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de SQL/Sales Analytics (SQLite)")
db_path = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de Python/sql-sales-analytics.db")

# 2) OJO: tu archivo tiene doble extensión .sql.sql
create_path = sql_dir / "01_create_tables.sql.sql"
insert_path = sql_dir / "02_insert_sample_data.sql"

print("DB:", db_path)
print("CREATE SQL:", create_path, "| exists:", create_path.exists())
print("INSERT SQL:", insert_path, "| exists:", insert_path.exists())

# 3) Crear/llenar DB
conn = sqlite3.connect(db_path)

create_sql = create_path.read_text(encoding="utf-8")
insert_sql = insert_path.read_text(encoding="utf-8")

conn.executescript(create_sql)
conn.executescript(insert_sql)

# 4) Verificar tablas
tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tablas en DB:\n", tablas)

# 5) Leer datos
clientes  = pd.read_sql("SELECT * FROM clientes", conn)
productos = pd.read_sql("SELECT * FROM productos", conn)
ventas    = pd.read_sql("SELECT * FROM ventas", conn)

print("\nClientes:\n", clientes.head())
print("\nProductos:\n", productos.head())
print("\nVentas:\n", ventas.head())
