CREATE TABLE products
(
    ProductID Int32,
    OrderID Int32,
    ProductPrice Float64,
    Quantity Int32
) ENGINE = Log;

CREATE TABLE "returns"
(
    orderId Int32,
    returnId Int32,
    returnDate Date
) ENGINE = Log;

CREATE TABLE orders
(
    order_id Int32,
    created_date Date,
    order_status_id Int32,
    is_test Int32
) ENGINE = Log;

CREATE TABLE orders_summary
(
    order_id Int32,
    created_date Date,
    order_status_id Int32,
    order_sum Float64,
    products Array(Int32),
    products_quantity Array(Int32),
    is_return Int32
) ENGINE = Log
