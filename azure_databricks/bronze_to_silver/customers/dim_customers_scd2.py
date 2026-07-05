# Databricks notebook source
# MAGIC %run ./config_00

# COMMAND ----------

dbutils.fs.rm(
    f"{silver_container}/dim_customers",
    True
)

# COMMAND ----------

cust_silver_path =f"{silver_container}/customers"
dim_cust_path=f"{silver_container}/dim_customers"

# COMMAND ----------

df_cust_initial=spark.read \
        .format("delta")\
        .option("versionAsOf",1)\
         .load(cust_silver_path)


# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

dimension_df =(
    df_cust_initial.withColumn("effective_date",current_timestamp())
                   .withColumn("end_date",lit(None).cast(TimestampType()))
                   .withColumn("is_current",lit(True))
)

# COMMAND ----------

dimension_df.write.mode("overwrite").format("delta").save(dim_cust_path)


# COMMAND ----------

# MAGIC %md
# MAGIC ## verifying

# COMMAND ----------

df_customerss=(
    spark.read.format("delta").load(cust_silver_path)
)

# COMMAND ----------

from pyspark.sql.functions import col
df_dim_customers=(
    spark.read.format("delta").load(dim_cust_path).filter(col("is_current")==True))


# COMMAND ----------

changed_df= (
    df_customerss.alias("new")
              .join(df_dim_customers.alias("old"),"customer_id")
              .filter("""
                      new.city <> old.city
                      OR new.state <> old.state
                      OR new.email <> old.email
                      OR new.customer_name <> old.customer_name

                      """)
              .select(
                  "new.customer_id",
                  "new.customer_name",
                  "new.city",
                  "new.state",
                  "new.email",
                  "new.created_at",
                  "new.updated_at",
                  "new.ingestion_timestamp"
              )
)

# COMMAND ----------

changed_df=changed_df.cache()
changed_df.count()

# COMMAND ----------

from delta.tables import DeltaTable 

dim_new_table=DeltaTable.forPath(spark,dim_cust_path)

# COMMAND ----------

(
    dim_new_table.alias("target")
    .merge(
        changed_df.alias("source"),
        """
        target.customer_id = source.customer_id
        AND target.is_current = true
        """
    )
    .whenMatchedUpdate(
        set={
            "is_current": "false",
            "end_date": "current_timestamp()"
        }
    )
    .execute()
)

# COMMAND ----------

df_dim_expired=(
    spark.read
         .format("delta")
         .load(dim_cust_path)
         .filter("is_current =false")
         .filter("end_date is not null")
)

# COMMAND ----------

changed_df = (
    df_customerss.alias("new")
        .join(
            df_dim_expired.alias("old"),
            "customer_id"
        )
        .filter(
            """
            new.city <> old.city
            OR new.state <> old.state
            OR new.email <> old.email
            OR new.customer_name <> old.customer_name
            """
        )
        .select(
            "new.customer_id",
            "new.customer_name",
            "new.city",
            "new.state",
            "new.email",
            "new.created_at",
            "new.updated_at",
            "new.ingestion_timestamp"
        )
)
changed_df.count()

# COMMAND ----------

new_records = (
    changed_df
        .withColumn(
            "effective_date",
            current_timestamp()
        )
        .withColumn(
            "end_date",
            lit(None).cast(TimestampType())
        )
        .withColumn(
            "is_current",
            lit(True)
        )
)

# COMMAND ----------

new_records.count()

# COMMAND ----------

new_records.write \
           .format("delta") \
           .mode("append") \
           .save(dim_cust_path)

# COMMAND ----------

spark.read.format("delta").load(dim_cust_path).count()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Appending