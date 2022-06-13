import numpy as np
import pandas as pd
from pandas import DataFrame

TECHNICAL_STATUSES = {63, 1003, 1004}


def transform_orders_df(df: DataFrame) -> DataFrame:
    """Remove test/technical orders and drop duplicates."""

    # filter test orders and orders with technical statuses
    exclude_test_orders_filter = df["is_test"] != 1
    exclude_technical_statuses_filter = ~df["order_status_id"].isin(TECHNICAL_STATUSES)

    df = df[exclude_test_orders_filter & exclude_technical_statuses_filter]

    # drop duplicates from orders with old date as order_id should be unique
    df.sort_values(by=["created_date"], inplace=True)
    df.drop_duplicates(subset=["order_id"], keep="last", inplace=True)

    return df


def transform_products_df(df: DataFrame) -> DataFrame:
    """Remove invalid products and calculate order sum."""

    # the same product could have different prices in different orders
    # exclude zero quantity orders
    df = df[df["Quantity"] > 0]

    # exclude orders with not positive prices
    df = df[df["ProductPrice"] > 0]

    # calculate order sum
    df["order_sum"] = df["ProductPrice"] * df["Quantity"]

    # aggregate list of products for each order
    df = df.groupby(["OrderID"], as_index=False).agg(
        {
            "order_sum": np.sum,
            "ProductID": lambda s: list(s),
            "Quantity": lambda s: list(s),
        }
    )

    return df


def transform_returns_df(df: DataFrame) -> DataFrame:
    """Remove returns and drop duplicates."""

    # drop cases when one return_id relates to several orders, save first by date
    df.sort_values(by=["returnDate"], inplace=True)
    df.drop_duplicates(subset=["returnId"], keep="first", inplace=True)

    # leave only one return per order not to cause errors on merge
    df.drop_duplicates(subset=["orderId"], inplace=True)

    return df


def merge_transformed_dfs(
    orders_df: DataFrame, products_df: DataFrame, returns_df: DataFrame
) -> DataFrame:
    """Merge orders, products and returns into single pandas DF."""

    orders_returns_df = pd.merge(
        orders_df, returns_df, how="left", left_on="order_id", right_on="orderId"
    )

    merged_df = pd.merge(
        orders_returns_df,
        products_df,
        how="left",
        left_on="order_id",
        right_on="OrderID",
    )

    return merged_df


def transform_merged_df(df: DataFrame) -> DataFrame:
    """Add additional columns and remove/rename columns,"""

    # transform returnId to is_return
    df.loc[df["returnId"].notnull(), "is_return"] = 1
    df.loc[df["returnId"].isnull(), "is_return"] = 0

    df.drop(
        ["returnDate", "orderId", "is_test", "OrderID", "returnId"],
        axis=1,
        inplace=True,
    )

    df.rename(
        columns={"ProductID": "products", "Quantity": "products_quantity"}, inplace=True
    )

    # drop orders without product details info
    df.dropna(inplace=True)

    return df
