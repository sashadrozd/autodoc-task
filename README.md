# autodoc-task

## Quick start
1. Specify parameters in docker-compose.yaml file:
 `AIRFLOW__SMTP__SMTP_MAIL_FROM`
 `AIRFLOW__SMTP__SMTP_PASSWORD`
 `AIRFLOW__SMTP__SMTP_HOST`
 `AIRFLOW__SMTP__SMTP_USER`
2. Specify parameter in EmailOperator in dag_1.py file: to
3. Run command: docker-compose up

## Task 2
1. Test orders and orders with technical statuses were dropped.
2. order_id is not unique in orders table. By logic should be unique. Duplicates were dropped based on date: save orders with newer date.   
3. Some products with same id have different prices. Maybe price depends on quantity. Nothing was done. 
4. Rows in product table with quantity equals 0 were dropped. 
5. Rows in product table with price less or equal to 0 were dropped. 
6. Return_ID is not unique in returns table. By logic one return can not correspond to several orders. Duplicates were dropped based on date: save returns with newer date.
7. Some orders in returns table have several returns. Good to check if sum of return is equal or less than sum of order. Duplicates was dropped based on order as amount of returns is not important for result_table. 
8. All tables have different naming policy. 
9. All tables were merged on order_id. Redundant columns were dropped, target columns were renamed. Row without product details info were dropped. 
 