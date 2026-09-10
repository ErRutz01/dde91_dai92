import pandas as pd
import os

from datetime import datetime
import datetime

from sqlalchemy import create_engine, text
import psycopg2

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

def load_data_to_staging(file) :

## Daten einlesen
    df = pd.read_csv(file, dtype={"Postal Code": str})


    ### Spaltennamen anpassen
    df = df.rename(
    columns={
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Postal Code": "postal_code",
        "Product ID": "product_id",
        "Product Name": "product_name",
        "Sub-Category": "sub_category",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        }
    )

    df.columns = df.columns.str.lower()
    df = df.dropna(subset=["postal_code"])

    ### Datentypen anpassen
    df["order_date"] = pd.to_datetime(df["order_date"], format="%d/%m/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%d/%m/%Y")



    ## finale Daten in die Staging-Tabelle schreiben
    df.to_sql("sales_order_item",
              con=engine,
              schema="staging",
              if_exists="append",
              index=False
              
     )
if __name__ == "__main__":
    file_path = os.path.join("raw_data/sales_order_item.csv")
    load_data_to_staging(file_path)
