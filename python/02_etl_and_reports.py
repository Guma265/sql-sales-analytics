import sqlite3
import pandas as pd
from pathlib import Path

# 1) Paths reales
sql_dir = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de SQL/Sales Analytics (SQLite)")
db_path = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de Python/sql-sales-analytics.db")

create_path = sql_dir / "01_create_tables.sql.sql"
insert_path = sql_dir / "02_insert_sample_data.sql"

print("DB:", db_path)
print("CREATE SQL:", create_path, "| exists:", create_path.exists())
print("INSERT SQL:", insert_path, "| exists:", insert_path.exists())

# 2) Conectar a SQLite
conn = sqlite3.connect(db_path)

# 3) (Opcional pero recomendado) Reconstruir DB para asegurar estado
create_sql = create_path.read_text(encoding="utf-8")
insert_sql = insert_path.read_text(encoding="utf-8")

conn.executescript(create_sql)
conn.executescript(insert_sql)

# 4) Cargar tablas en pandas  🔴 ESTO FALTABA
clientes  = pd.read_sql("SELECT * FROM clientes", conn)
productos = pd.read_sql("SELECT * FROM productos", conn)
ventas    = pd.read_sql("SELECT * FROM ventas", conn)

# 5) Análisis en pandas
productos_ren = productos.rename(columns={"nombre": "producto"})

ventas_prod = ventas.merge(productos_ren, on="id_producto", how="left")

ingresos_por_producto = (
    ventas_prod
    .groupby("producto")["precio"]
    .sum()
    .reset_index(name="ingresos")
    .sort_values("ingresos", ascending=False)
)

print("\nIngresos por producto:")
print(ingresos_por_producto)
