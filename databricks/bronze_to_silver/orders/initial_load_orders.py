# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

bronze_path =f"{bronze_container}/orders"
silver_path =f"{silver_container}/orders"

# COMMAND ----------

df=spark.read.format("csv").option("header",True).load(bronze_path)
df.display()


# COMMAND ----------

from pyspark.sql.functions import cast,col
from pyspark.sql.types import TimestampType
df_orders = df.withColumn("order_date",col("order_date").cast("timestamp")) \
              .withColumn("updated_at",col("updated_at").cast("timestamp")) \
              .withColumn("created_at",col("created_at").cast("timestamp")) 


# COMMAND ----------

before =df_orders.count()
df_orders=(
    df_orders.filter(col("order_id").isNotNull())
             .dropDuplicates(["order_id"])
)
after=df_orders.count()
print(f"Duplicates Removed: {before - after}")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp
df_orders=df_orders.withColumn("ingestion_timestamp",current_timestamp())

# COMMAND ----------

df_orders.write.mode("overwrite").format("delta").save(silver_path)

# COMMAND ----------

spark.read.format("delta").load(silver_path).count()