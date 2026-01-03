import sqlite3
from pathlib import Path
import pandas as pd
import logging


# -------------------------
# CONFIG
# -------------------------
SQL_DIR = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de SQL/Sales Analytics (SQLite)")
DB_PATH = Path("/Users/guma/Desktop/Aprendiendo Python y SQL/Aprendizaje de Python/sql-sales-analytics.db")

CREATE_SQL_PATH = SQL_DIR / "01_create_tables.sql.sql"
INSERT_SQL_PATH = SQL_DIR / "02_insert_sample_data.sql"

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# -------------------------
# LOGGING
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------
# DB BUILD
# -------------------------
def build_db(conn: sqlite3.Connection) -> None:
    """Rebuild SQLite DB from SQL scripts (reproducible)."""
    if not CREATE_SQL_PATH.exists():
        raise FileNotFoundError(f"No existe: {CREATE_SQL_PATH}")
    if not INSERT_SQL_PATH.exists():
        raise FileNotFoundError(f"No existe: {INSERT_SQL_PATH}")

    create_sql = CREATE_SQL_PATH.read_text(encoding="utf-8")
    insert_sql = INSERT_SQL_PATH.read_text(encoding="utf-8")

    conn.executescript(create_sql)
    conn.executescript(insert_sql)
    logger.info("DB reconstruida desde scripts.")


def load_tables(conn: sqlite3.Connection) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load clientes/productos/ventas as DataFrames."""
    clientes = pd.read_sql("SELECT * FROM clientes", conn)
    productos = pd.read_sql("SELECT * FROM productos", conn)
    ventas = pd.read_sql("SELECT * FROM ventas", conn)

    logger.info(f"Tablas cargadas | clientes={len(clientes)} productos={len(productos)} ventas={len(ventas)}")
    return clientes, productos, ventas


# -------------------------
# DATA QUALITY
# -------------------------
def run_quality_checks(clientes: pd.DataFrame, productos: pd.DataFrame, ventas: pd.DataFrame) -> None:
    """Raise AssertionError if any quality check fails."""
    # A) Nulos en claves
    assert ventas["id_cliente"].isna().sum() == 0, "❌ Hay ventas sin cliente"
    assert ventas["id_producto"].isna().sum() == 0, "❌ Hay ventas sin producto"

    # B) Duplicados (mismo cliente, producto, fecha)
    dup = ventas.duplicated(subset=["id_cliente", "id_producto", "fecha"]).sum()
    assert dup == 0, f"❌ Hay {dup} ventas duplicadas"

    # C) Precios válidos
    assert productos["precio"].isna().sum() == 0, "❌ Hay precios nulos"
    assert (productos["precio"] <= 0).sum() == 0, "❌ Hay precios inválidos (<=0)"

    # D) Campos críticos no vacíos
    assert clientes["nombre"].astype(str).str.strip().eq("").sum() == 0, "❌ Clientes con nombre vacío"
    assert productos["nombre"].astype(str).str.strip().eq("").sum() == 0, "❌ Productos con nombre vacío"

    # E) Integridad referencial (ventas huérfanas)
    clientes_ids = set(clientes["id_cliente"])
    productos_ids = set(productos["id_producto"])
    assert (~ventas["id_cliente"].isin(clientes_ids)).sum() == 0, "❌ Ventas con cliente inexistente"
    assert (~ventas["id_producto"].isin(productos_ids)).sum() == 0, "❌ Ventas con producto inexistente"

    logger.info("✔ Data quality checks pasados.")


# -------------------------
# TRANSFORMS & REPORTS
# -------------------------
def build_ventas_enriquecidas(clientes: pd.DataFrame, productos: pd.DataFrame, ventas: pd.DataFrame) -> pd.DataFrame:
    clientes_ren = clientes.rename(columns={"nombre": "cliente"})
    productos_ren = productos.rename(columns={"nombre": "producto"})

    ventas_enriq = (
        ventas
        .merge(clientes_ren[["id_cliente", "cliente", "ciudad"]], on="id_cliente", how="left")
        .merge(productos_ren[["id_producto", "producto", "precio"]], on="id_producto", how="left")
    )

    # Mes YYYY-MM
    ventas_enriq["mes"] = ventas_enriq["fecha"].astype(str).str.slice(0, 7)
    logger.info("Ventas enriquecidas construidas.")
    return ventas_enriq


def report_ingresos_por_producto(ventas_enriq: pd.DataFrame) -> pd.DataFrame:
    rep = (
        ventas_enriq
        .groupby("producto")["precio"]
        .sum()
        .reset_index(name="ingresos")
        .sort_values("ingresos", ascending=False)
    )
    return rep


def report_ventas_por_cliente_mes(ventas_enriq: pd.DataFrame) -> pd.DataFrame:
    rep = (
        ventas_enriq
        .groupby(["cliente", "mes"])
        .agg(
            total_ventas=("id_venta", "count"),
            ingresos=("precio", "sum")
        )
        .reset_index()
        .sort_values(["cliente", "mes"])
    )
    return rep


def report_ranking_clientes(ventas_enriq: pd.DataFrame) -> pd.DataFrame:
    rep = (
        ventas_enriq
        .groupby(["id_cliente", "cliente"])
        .agg(gasto_total=("precio", "sum"))
        .reset_index()
        .sort_values("gasto_total", ascending=False)
    )
    rep["ranking"] = rep["gasto_total"].rank(method="dense", ascending=False).astype(int)
    return rep


# -------------------------
# EXPORT
# -------------------------
def export_csv(df: pd.DataFrame, filename: str) -> None:
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    logger.info(f"Exportado: {path}")


# -------------------------
# MAIN
# -------------------------
def main() -> None:
    logger.info("Inicio pipeline ETL...")

    conn = sqlite3.connect(DB_PATH)
    try:
        build_db(conn)
        clientes, productos, ventas = load_tables(conn)
        run_quality_checks(clientes, productos, ventas)

        ventas_enriq = build_ventas_enriquecidas(clientes, productos, ventas)

        ingresos_prod = report_ingresos_por_producto(ventas_enriq)
        ventas_cli_mes = report_ventas_por_cliente_mes(ventas_enriq)
        ranking_cli = report_ranking_clientes(ventas_enriq)

        export_csv(ventas_enriq, "ventas_enriquecidas.csv")
        export_csv(ingresos_prod, "ingresos_por_producto.csv")
        export_csv(ventas_cli_mes, "ventas_por_cliente_mes.csv")
        export_csv(ranking_cli, "ranking_clientes.csv")

        logger.info("✅ Pipeline completado.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
