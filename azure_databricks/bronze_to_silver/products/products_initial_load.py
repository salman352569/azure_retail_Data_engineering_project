# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

bronze_path=f"{bronze_container}/products"
df=(
    spark.read
        .option("header","true")
        .format("csv")
        .load(bronze_path)
)
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Rounding price column

# COMMAND ----------

from pyspark.sql.functions import round,col
df_products=df.withColumn("price",
                          round(col("price"),2))
#display(df_products)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Adding ingestion timestamp Columns & casting columns

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,cast,col
df_products =(
df_products.withColumn("ingestion_timestamp",current_timestamp())
           .withColumn("created_at",col("created_at").cast("timestamp"))
           .withColumn("updated_at",col("updated_at").cast("timestamp"))

)

# COMMAND ----------

df_products=df_products.dropDuplicates(["product_id"])


# COMMAND ----------

from pyspark.sql.functions import trim,col,upper
df_products=(
df_products.withColumn("product_name",trim(col("product_name")))
           .withColumn("category",upper(trim(col("category"))))
)
#df_products.display()

# COMMAND ----------

silver_path=f"{silver_container}/products"
df_old_1.write \
        .mode("overwrite")\
        .format("delta")\
        .save(silver_path)

# COMMAND ----------

from pyspark.sql.functions import col
df=df_old_1.drop(col("load_date"))
df.printSchema()
df.write.mode("delta").save(silver_path)

# COMMAND ----------

df.write.format("delta").mode("overwrite").save(silver_path)