from sqlalchemy import create_engine, text

from scripts.lib_py.load_staging import load_data_to_staging
from scripts.lib_py.load_data_mart import load_data_mart
from scripts.lib_py.normalisierung import tabellen_normalisieren

engine = create_engine("postgresql://EricRutz12:4hFd98Tm!120101@127.0.0.1:5432/sales_order_item")

def execute_sql(file_path):
    with open(file_path, "r", encoding="UTF8") as f:
        sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

def run_pipeline():

    sql_files = [
        "init-db/init.sql",
        "init-db/core-area_create-tables.sql",
        "init-db/data-mart_create-tables.sql"
    ]

    for file in sql_files:
        execute_sql(file)

    load_data_to_staging("raw_data/sales_order_item.csv")
    tabellen_normalisieren("data/cleaned_sales_order_item.csv")
    load_data_mart("data/cleaned_sales_order_item.csv")

if __name__ == "__main__":
    run_pipeline()
