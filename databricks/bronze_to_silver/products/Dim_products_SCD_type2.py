# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

silver_product_path=(f"{silver_container}/products")
dim_product_path=(f"{silver_container}/dim_products")

# COMMAND ----------

df_products=(
    spark.read 
         .format("delta")
         .load(silver_product_path)
)
df_products.count()

# COMMAND ----------

from pyspark.sql.functions import col,current_timestamp,lit
from pyspark.sql.types import TimestampType
dim_df =(
df_products.withColumn("effective_date",current_timestamp())
           .withColumn("end_date",lit(None).cast(TimestampType()))
           .withColumn("is_current",lit(True))
)

# COMMAND ----------

dim_df.write.mode("overwrite").format("delta").save(dim_product_path)

# COMMAND ----------

df_latest=(
    spark.read.format("delta").load(silver_product_path)
)


# COMMAND ----------

from pyspark.sql.functions import col
df_dim_products=spark.read.format("delta").load(dim_product_path).filter(col("is_current")==True)


# COMMAND ----------

changed_df=(
    df_latest.alias("new")
    .join(df_dim_products.alias("old"),
          "product_id")
    .filter("""
            new.product_name <> old.product_name
        OR  new.category <> old.category
        OR  new.price <> old.price
         """
         )
    .select("new.*")
    .cache()
)
changed_df.count()

# COMMAND ----------

from delta.tables import DeltaTable

dim_table=DeltaTable.forPath(spark,dim_product_path)

(
    dim_table.alias("target")
    .merge(
        changed_df.alias("new"),
        """
        target.product_id = new.product_id
        AND target.is_current =true
        """
    )
    .whenMatchedUpdate(
        set={
            "is_current":"false",
            "end_date":"current_timestamp()"
        }
        )
    .execute()
)

# COMMAND ----------

new_records =(
    changed_df
    .withColumn("effective_date",current_timestamp())
    .withColumn("end_date",lit(None).cast(TimestampType()))
    .withColumn("is_current",lit(True))
    
)

# COMMAND ----------

new_records.write \
          .format("delta") \
          .mode("append") \
          .save(dim_product_path)