from pandas import DataFrame
import datacompy


def transform_orders_df(df: DataFrame) -> DataFrame:
    df['order_conv_sum'] = df['currency'] * df['order_sum']
    df.drop(['order_sum', 'currency'], axis=1, inplace=True)

    return df


def generate_report(df1: DataFrame, df2: DataFrame):
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['order_id'],
        df1_name='orders_generated',
        df2_name='orders_original'
    )
    s = compare.report()
    with open('/data/report.txt', 'w+') as report_file:
        report_file.write(s)
