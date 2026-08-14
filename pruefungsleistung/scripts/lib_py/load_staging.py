import pandas as pd
import os

from datetime import datetime
import datetime

from sqlalchemy import create_engine, text
import psycopg2


engine = create_engine('postgresql://EricRutz12:4hFd98Tm!120101@127.0.0.1:5432/sales_order_item')

def load_data_to_staging(file) :

## Daten einlesen
    df = pd.read_csv(file)

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

    df = df.dropna(subset=["postal_code"])
    df.to_csv("data/cleaned_sales_order_item.csv", index=False)

if __name__ == "__main__":
    file_path = os.path.join("raw_data/sales_order_item.csv")
    load_data_to_staging(file_path)
