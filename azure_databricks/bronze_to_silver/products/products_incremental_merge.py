# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

from datetime import date

today=date.today().strftime("%Y-%m-%d")

bronze_path=(
    f"{bronze_container}/products/load_date={today}"

)


# COMMAND ----------

df_incremental =(
    spark.read.option("header",True).format("csv").load(bronze_path)
)
display(df_incremental)
print(f"count:{df_incremental.count()}")

# COMMAND ----------

from pyspark.sql.functions import col,cast,current_timestamp,lit
df_incremental=(
    df_incremental.withColumn("created_at",col("created_at").cast("timestamp"))
                  .withColumn("updated_at",col("updated_at").cast("timestamp"))
                  .dropDuplicates(["product_id"])
                  .withColumn("ingestion_timestamp",current_timestamp())
)
df_incremental.display()

# COMMAND ----------

df_incremental.printSchema()

# COMMAND ----------

from delta.tables  import DeltaTable 
silver_path=f"{silver_container}/products"
delta_table=DeltaTable.forPath(spark,silver_path)

(
    delta_table.alias("target")
    .merge(df_incremental.alias("source"),
           "target.product_id=source.product_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)   


# COMMAND ----------

spark.read.format("delta").load(silver_path).count()