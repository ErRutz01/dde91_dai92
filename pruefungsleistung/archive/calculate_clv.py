import pandas as pd
import numpy as np
import os

from datetime import datetime
import datetime


def clv_berechnen(df):

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed")

    df["order_year"] = df["order_date"].dt.year

    ## customer_dim - table
    customer_dim = df[["customer_id", "segment", "customer_name"]].copy()
    customer_dim = customer_dim.drop_duplicates(subset=["customer_id"])

    ## avrg_puchase_value
    sum_sales_value_df = df.groupby(["customer_id"], as_index=False).agg({
        'sales': 'sum'
    })

    sum_sales_value_df = sum_sales_value_df.rename(
        columns={
            "sales": "sales_sum",
        }
    )

    ## order_count
    order_count_table_df = df.pivot_table( values= ["order_id"], index = "customer_id", aggfunc="nunique").reset_index()

    order_count_table_df = order_count_table_df.rename(
        columns={
            "order_id": "order_count",
        }
    )

    ## customer_lifespan
    customer_lifespan_df = df.pivot_table( values= ["order_year"], index = "customer_id", aggfunc="nunique").reset_index()
    
    customer_lifespan_df = customer_lifespan_df.rename(
        columns={
            "order_year": "customer_lifespan",
        }
    )

    ## Merge df

    customer_dim_merge1 = customer_dim.merge(sum_sales_value_df[["customer_id","sales_sum"]],how ="left", on="customer_id")

    customer_dim_merge2 = customer_dim_merge1.merge(order_count_table_df[["customer_id","order_count"]],how ="left", on="customer_id")

    customer_dim_merge3 = customer_dim_merge2.merge(customer_lifespan_df[["customer_id","customer_lifespan"]],how ="left", on="customer_id")

    ## AVRG Puchase Value berechnen
    customer_dim_merge3["avrg_purchase_value"] = customer_dim_merge3["sales_sum"]/customer_dim_merge3["order_count"]
    
    ## Purchase Frequency berechnen
    customer_dim_merge3["purchase_frequency"] = customer_dim_merge3["order_count"]/customer_dim_merge3["customer_lifespan"]

    ## CLV berechnen
    customer_dim_merge3["clv"]  = customer_dim_merge3["avrg_purchase_value"]*customer_dim_merge3["purchase_frequency"]*customer_dim_merge3["customer_lifespan"]
    customer_dim_merge3["clv"] = np.log1p(customer_dim_merge3["clv"])

    ## Finaler df
    final_customer_dim = customer_dim_merge3[["customer_id", "segment","customer_name", "avrg_purchase_value", "customer_lifespan", "purchase_frequency", "clv"]].copy()

    return final_customer_dim

if __name__ == "__main__":
    file_path = os.path.join("raw_data/sales_order_item.csv")
    clv_berechnen(file_path)