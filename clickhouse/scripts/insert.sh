#!/bin/bash
set -e

cat '/data/orders.csv' | clickhouse-client --query="INSERT INTO orders FORMAT CSVWithNames"
cat '/data/products.csv' | clickhouse-client --query="INSERT INTO products FORMAT CSVWithNames"
cat '/data/returns.csv' | clickhouse-client --query="INSERT INTO returns FORMAT CSVWithNames"
