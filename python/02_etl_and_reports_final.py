import sqlite3
from pathlib import Path
import pandas as pd
import logging

# -------------------------
# PATHS (RELATIVOS AL REPO)
# -------------------------
ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "schema"
DATA_DIR = ROOT / "data"
DB_PATH = ROOT / "sql-sales-analytics.db"

CREATE_SQL_PATH = SQL_DIR / "01_create_tables.sql"
INSERT_SQL_PATH = DATA_DIR / "02_insert_sample_data.sql"

OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------
# LOGGING
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# -------------------------
# DB BUILD
# -------------------------
def build_db(conn):
    create_sql = CREATE_SQL_PATH.read_text(encoding="utf-8")
    insert_sql = INSERT_SQL_PATH.read_text(encoding="utf-8")
    conn.executescript(create_sql)
    conn.executescript(insert_sql)
    logger.info("DB reconstruida desde scripts.")

def load_tables(conn):
    clientes = pd.read_sql("SELECT * FROM clientes", conn)
    productos = pd.read_sql("SELECT * FROM productos", conn)
    ventas = pd.read_sql("SELECT * FROM ventas", conn)
    logger.info(f"Tablas cargadas | clientes={len(clientes)} productos={len(productos)} ventas={len(ventas)}")
    return clientes, productos, ventas

def run_quality_checks(clientes, productos, ventas):
    assert ventas["id_cliente"].isna().sum() == 0
    assert ventas["id_producto"].isna().sum() == 0
    assert ventas.duplicated(subset=["id_cliente","id_producto","fecha"]).sum() == 0
    assert productos["precio"].isna().sum() == 0
    assert (productos["precio"] <= 0).sum() == 0
    assert clientes["nombre"].astype(str).str.strip().eq("").sum() == 0
    assert productos["nombre"].astype(str).str.strip().eq("").sum() == 0
    assert (~ventas["id_cliente"].isin(set(clientes["id_cliente"]))).sum() == 0
    assert (~ventas["id_producto"].isin(set(productos["id_producto"]))).sum() == 0
    logger.info("✔ Data quality checks pasados.")

def build_ventas_enriq(clientes, productos, ventas):
    c = clientes.rename(columns={"nombre":"cliente"})
    p = productos.rename(columns={"nombre":"producto"})
    df = (ventas
          .merge(c[["id_cliente","cliente","ciudad"]], on="id_cliente", how="left")
          .merge(p[["id_producto","producto","precio"]], on="id_producto", how="left"))
    df["mes"] = df["fecha"].astype(str).str.slice(0,7)
    return df

def export_csv(df, name):
    path = OUTPUT_DIR / name
    df.to_csv(path, index=False)
    logger.info(f"Exportado: {path}")

def main():
    logger.info("Inicio pipeline ETL...")
    conn = sqlite3.connect(DB_PATH)
    try:
        build_db(conn)
        clientes, productos, ventas = load_tables(conn)
        run_quality_checks(clientes, productos, ventas)

        ventas_enriq = build_ventas_enriq(clientes, productos, ventas)

        ingresos_prod = (ventas_enriq.groupby("producto")["precio"].sum()
                          .reset_index(name="ingresos").sort_values("ingresos", ascending=False))
        ventas_cli_mes = (ventas_enriq.groupby(["cliente","mes"])
                          .agg(total_ventas=("id_venta","count"), ingresos=("precio","sum"))
                          .reset_index().sort_values(["cliente","mes"]))
        ranking_cli = (ventas_enriq.groupby(["id_cliente","cliente"])
                       .agg(gasto_total=("precio","sum")).reset_index()
                       .sort_values("gasto_total", ascending=False))
        ranking_cli["ranking"] = ranking_cli["gasto_total"].rank(method="dense", ascending=False).astype(int)

        export_csv(ventas_enriq, "ventas_enriquecidas.csv")
        export_csv(ingresos_prod, "ingresos_por_producto.csv")
        export_csv(ventas_cli_mes, "ventas_por_cliente_mes.csv")
        export_csv(ranking_cli, "ranking_clientes.csv")

        logger.info("✅ Pipeline completado.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
