# autodoc-task

**Airflow credentials:**

| Key      | Value    |
| ---------| ---------|
| Username | airflow  |
| Password | airflow  |

**Clickhouse DB credentials:**

| Key      | Value    |
| ---------| ---------|
| Host     | localhost|
| Port     | 8123     |
| User     | default  |

| Password |          |
| Database | default  |

## Quick start
1. Specify email parameters in the `docker-compose.yaml` file ([here](https://github.com/sashadrozd/autodoc-task/blob/main/docker-compose.yaml#L18)):
 - `AIRFLOW__SMTP__SMTP_HOST`;
 - `AIRFLOW__SMTP__SMTP_MAIL_FROM`;
 - `AIRFLOW__SMTP__SMTP_PASSWORD`;
 - `AIRFLOW__SMTP__SMTP_USER`;
 - `EMAIL_TO`
2. Run command: `docker-compose up`;
3. Visit http://localhost:8080/;

### Task 1
1. Enable `dag_1` through airflow UI;
2. Explore report sent to your email address.

### Task 2
1. Enable `dag_2` through airflow UI;
2. Explore data in the `orders_summary` table (run
`select * from orders_summary;`).

#### Summary
1. Test orders and orders with technical statuses were dropped;
2. `order_id` is not unique in the `orders` table. By logic should be unique. Duplicates were dropped based on date: save orders with newer date;   
3. Some products with same `id` have different prices. Maybe price depends on quantity. Nothing was done;
4. Rows in the `product` table with quantity equals 0 were dropped;
5. Rows in the `product` table with price less or equal to 0 were dropped; 
6. `Return_ID` is not unique in returns table. By logic one return can not correspond to several orders. Duplicates were dropped based on date: save returns with newer date;
7. Some orders in the `returns` table have several returns. Good to check if sum of return is equal or less than sum of order. Duplicates was dropped based on order as amount of returns is not important for the result table; 
8. All tables have different naming policy;
9. All tables were merged on `order_id`. Redundant columns were dropped, target columns were renamed. Row without product details info were dropped. 
 