# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

customer_bronze_path=(
    f"{bronze_container}/customers"
)
df=(
    spark.read 
    .option("header",True)
    .csv(customer_bronze_path)

)
df.display()

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,col,cast
df_clean =(
    df
    .dropDuplicates(["customer_id"])
    .filter(col("customer_id").isNotNull())
    .filter(col("customer_name").isNotNull())
    .withColumn(
        "updated_at",
        col("updated_at").cast("timestamp")
    )
    .withColumn("created_at",col("created_at").cast("timestamp"))
    .withColumn("ingestion_timestamp",current_timestamp())
)   

# COMMAND ----------

customer_silver_path = f"{silver_container}/customers"

df_clean.write.format("delta").mode("overwrite").save(customer_silver_path)