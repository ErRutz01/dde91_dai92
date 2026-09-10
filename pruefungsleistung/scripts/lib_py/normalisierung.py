import pandas as pd
import os
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

query = "SELECT * FROM staging.sales_order_item"

def tabellen_normalisieren(query):

    df = pd.read_sql(query , con = engine)

    # Tabellen erstellen

    ## customer
    customer_df = df[["customer_id", "customer_name", "segment"]].copy()
    customer_df = customer_df.drop_duplicates(subset=["customer_id"])

    ## location
    location_df = df[["postal_code", "city", "state", "country", "region"]].copy()
    location_df = location_df.drop_duplicates(subset=["postal_code"])

    ## category
    category_df = df[["sub_category", "category"]].copy()
    category_df = category_df.drop_duplicates(subset=["sub_category"])

    ## product
    product_df = df[["product_id", "sub_category","product_name"]].copy()
    product_df = product_df.drop_duplicates(subset=["product_id"])

    ## order
    order_df = df[["order_id", "customer_id","postal_code", "order_date", "ship_date", "ship_mode"]].copy().dropna()
    order_df = order_df.drop_duplicates(subset=["order_id"])

    ## bruecken_tabelle
    bruecke_df = df.groupby(["order_id", "product_id"], as_index=False)["sales"].sum()

    # DataFrames in Datenbank schreiben

    df_list = [
        customer_df,
        location_df,
        category_df,
        product_df,
        order_df,
        bruecke_df
    ]

    table_names = [
        "customer",
        "location",
        "category",
        "product",
        "orders",
        "bruecken_tabelle"
    ]

    for df_element, name_element in zip(df_list, table_names):

        df_element.to_sql(name_element,
            con=engine,
            schema="core",
            if_exists="append",
            index=False
            
            )

if __name__ == "__main__":
    tabellen_normalisieren(query)