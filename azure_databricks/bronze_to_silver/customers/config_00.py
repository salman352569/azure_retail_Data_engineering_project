# Databricks notebook source
storage_account = "retailstorage352"
storage_key ="YOUR_STORAGE_ACCOUNT_KEY"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_key,
)
bronze_container =f"abfss://bronze@{storage_account}.dfs.core.windows.net"
silver_container = f"abfss://silver@{storage_account}.dfs.core.windows.net"
gold_container = f"abfss://gold@{storage_account}.dfs.core.windows.net"
