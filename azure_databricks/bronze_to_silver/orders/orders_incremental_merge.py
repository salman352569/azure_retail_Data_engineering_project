# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

from datetime import date
today= date.today().strftime("%Y-%m-%d")

bronze_path=f"{bronze_container}/orders/load_date={today}"

df_incremental=(
    spark.read.format("csv").option("header",True).load(bronze_path)
)

# COMMAND ----------

df_incremental.display()

# COMMAND ----------

from pyspark.sql.functions import col,cast,current_timestamp,lit
df_incremental= df_incremental.withColumn("created_at",col("created_at").cast("timestamp"))\
                              .withColumn("updated_at",col("updated_at").cast("timestamp"))\
                              .withColumn("ingestion_timestamp",current_timestamp())\
                              .withColumn("load_date",lit(today))
df_incremental.printSchema()

# COMMAND ----------

from delta.tables import DeltaTable 
silver_path=f"{silver_container}/orders"
delta_table =DeltaTable.forPath(spark,silver_path)

(delta_table.alias("target")
 .merge(df_incremental.alias("source"),
        "target.order_id = source.order_id"
        )
         .whenMatchedUpdateAll()
         .whenNotMatchedInsertAll()
         .execute()
 )
          

# COMMAND ----------

