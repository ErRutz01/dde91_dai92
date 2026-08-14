import os
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("postgresql://EricRutz12:4hFd98Tm!120101@127.0.0.1:5432/sales_order_item")

def tabellen_normalisieren(file):

    df = pd.read_csv(file)

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
    file_path = os.path.join("data/cleaned_sales_order_item.csv")
    tabellen_normalisieren(file_path)