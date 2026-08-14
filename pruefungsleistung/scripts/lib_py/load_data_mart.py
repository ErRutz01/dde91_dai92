import pandas as pd
import os

from datetime import datetime
import datetime

from sqlalchemy import create_engine, text
import psycopg2

from scripts.lib_py.calculate_clv import clv_berechnen

engine = create_engine("postgresql://EricRutz12:4hFd98Tm!120101@127.0.0.1:5432/sales_order_item")

def load_data_mart(file):

    df = pd.read_csv(file)

    

    ## customer_dim
    customer_dim_df = clv_berechnen(df)

    ##standort_dim
    standort_dim_df = df[["postal_code", "city", "state", "region"]].copy()
    standort_dim_df = standort_dim_df.drop_duplicates(subset=["postal_code"]).dropna()

    ## product_dim
    produkt_dim_df = df[["product_id", "product_name","category", "sub_category"]].copy()
    produkt_dim_df = produkt_dim_df.drop_duplicates(subset=["product_id"])

    ## shipping_dim
    shipping_dim_df = df[["order_id", "order_date", "ship_date", "ship_mode"]].copy()
    shipping_dim_df = shipping_dim_df.drop_duplicates(subset=["order_id"])

    ### Anzahl an Tagen bis zur Zurstellerung berechnen
    shipping_dim_df["delivery_days"] = (shipping_dim_df["ship_date"] - shipping_dim_df["order_date"]).dt.days

    ## main_table
    main_table = df.groupby(["order_id", "product_id", "postal_code", "customer_id", "country"], as_index=False)["sales"].sum().dropna()

    df_list = [
        customer_dim_df,
        standort_dim_df,
        produkt_dim_df,
        shipping_dim_df,
        main_table,
    ]

    table_names = [
        "customer_dim",
        "location_dim",
        "product_dim",
        "shipping_dim",
        "main_table",
    ]

    for df_element, name_element in zip(df_list, table_names):

        df_element.to_sql(name_element,
            con=engine,
            schema="mart",
            if_exists="append",
            index=False
            
            )

if __name__ == "__main__":
    file_path = os.path.join("data/cleaned_sales_order_item.csv")
    load_data_mart(file_path) 

