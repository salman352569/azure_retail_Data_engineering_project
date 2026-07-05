# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

bronze_path=f"{bronze_container}/order_items"
silver_path=f"{silver_container}/order_items"

# COMMAND ----------

df_load=(
    spark.read.format("csv").option("header",True).load(bronze_path)
)


# COMMAND ----------

print(f"Schema: {df_load.printSchema()}")
display(df_load)

# COMMAND ----------

from pyspark.sql.functions import round,col
df_load=df_load.withColumn("sales_amount",round(col("sales_amount"),2))
display(df_load)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,cast

df_silver =df_load.withColumn("created_at",col("created_at").cast("timestamp"))\
                  .withColumn("updated_at",col("updated_at").cast("timestamp")) \
                  .withColumn("ingestion_timetamp",current_timestamp())

# COMMAND ----------

df_silver.write.mode("overwrite").format("delta").save(silver_path)

# COMMAND ----------

spark.read.format("delta").load(silver_path).count()