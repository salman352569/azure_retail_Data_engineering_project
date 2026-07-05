# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

customer_path=f"{silver_container}/dim_customers"
product_path=f"{silver_container}/dim_products"
orders_path=f"{silver_container}/orders"
order_items_path=f"{silver_container}/order_items"



# COMMAND ----------

dim_customer=spark.read.format("delta").load(customer_path)
dim_products=spark.read.format("delta").load(product_path)
dim_orders=spark.read.format("delta").load(orders_path)
dim_order_items=spark.read.format("delta").load(order_items_path)

# COMMAND ----------

print(dim_customer.count())
print(dim_products.count())
print(dim_orders.count())
print(dim_order_items.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## GOLD DIM Customers

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.window import Window
customer_window=Window.orderBy("customer_id")
gold_dim_customers=dim_customer.filter(col("is_current") ==True)\
                    .select(
                        "customer_id",
                        "customer_name",
                        "city",
                        "state",
                        "email"
                        )\
                    .withColumn("customer_key",row_number().over(customer_window))


# COMMAND ----------

dim_products.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## GOLD DIM PRODUCTS

# COMMAND ----------

from pyspark.sql.functions import col
product_window=Window.orderBy("product_id")
gold_dim_products= dim_products.filter(col("is_current") == True) \
                               .select(
                                   "product_id",
                                   "product_name",
                                   "category",
                                   "price"
                               )     \
                                .withColumn("product_key",
                                            row_number().over(product_window))    

# COMMAND ----------

from pyspark.sql.functions import sequence,explode

date_df =spark.sql("""
                   select explode(
                       sequence(
                           to_date('2023-01-01'),
                           to_date('2027-12-31'),
                           interval 1 day
                       )
                   ) AS date 
                   """)

# COMMAND ----------

# MAGIC %md
# MAGIC ## GOLD DIM DATE

# COMMAND ----------

from pyspark.sql.functions import *
gold_dim_date= (
    date_df
    .withColumn("date_key",date_format("date","yyyyMMdd").cast("int"))
    .withColumn("year",year("date"))
    .withColumn("quarter",quarter("date"))
    .withColumn("month",month("date"))
    .withColumn("month_name",date_format("date","MMMM"))
    .withColumn("day",dayofmonth("date"))
    .withColumn("week",weekofyear("date"))
    .withColumn("day_name",date_format("date","EEEE"))
)



# COMMAND ----------

# MAGIC %md
# MAGIC ## ##FACT SALES

# COMMAND ----------

fact_sales=(
    dim_orders.alias("o")
    .join(dim_order_items.alias("oi"),"order_id")
)

# COMMAND ----------

fact_sales=(
    fact_sales.join(gold_dim_customers.select("customer_key","customer_id"),"customer_id")
)

# COMMAND ----------

fact_sales=(
    fact_sales.join(gold_dim_products.select("product_key","product_id"),"product_id")
)

# COMMAND ----------

fact_sales =fact_sales.withColumn("date_key",date_format("order_date","yyyyMMdd").cast("int"))

# COMMAND ----------

gold_fact_sales= fact_sales.select(
    "order_item_id",
    "order_id",
    "customer_key",
    "product_key",
    "date_key",
    col("quantity").cast("int").alias("quantity"),
    "sales_amount"
)


# COMMAND ----------

print(gold_dim_customers.count())
print(gold_dim_products.count())
print(gold_dim_date.count())
print(fact_sales.count())

# COMMAND ----------

gold_customer_path=f"{gold_container}/dim_customers"
gold_products_path=f"{gold_container}/dim_products"
gold_date_path=f"{gold_container}/dim_date"
gold_fact_path=f"{gold_container}/Fact_sales"

# COMMAND ----------

gold_dim_customers.write.mode("overwrite").format("delta").save(gold_customer_path)
gold_dim_products.write.mode("overwrite").format("delta").save(gold_products_path)
gold_dim_date.write.mode("overwrite").format("delta").save(gold_date_path)
gold_fact_sales.write.mode("overwrite").format("delta").save(gold_fact_path)