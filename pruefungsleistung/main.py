from sqlalchemy import create_engine, text
import os


from scripts.lib_py.load_staging import load_data_to_staging
from scripts.lib_py.normalisierung import tabellen_normalisieren

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

def execute_sql(file_path):
    with open(file_path, "r", encoding="UTF8") as f:
        sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

def run_pipeline():

    init_sql_files = [
        "init-db/init.sql",
        "init-db/staging-area_create-table.sql",
        "init-db/core-area_create-tables.sql",
        "init-db/data-mart_create-tables.sql",
        "scripts/sql/truncate_core.sql",
        "scripts/sql/truncate_staging.sql"
    ]

    data_update_sql_files = [
        "scripts/sql/load_core-mart.sql",
        "scripts/sql/mart_kpi-update.sql"
        ]

    for file in init_sql_files:
        execute_sql(file)

    load_data_to_staging("raw_data/sales_order_item.csv")
    tabellen_normalisieren("SELECT * FROM staging.sales_order_item")

    for file2 in data_update_sql_files:
        execute_sql(file2)

if __name__ == "__main__":
    run_pipeline()
