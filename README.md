# 🚀 End-to-End Azure Retail Data Engineering Project

## 📌 Project Overview

This project demonstrates an end-to-end modern data engineering pipeline built on Microsoft Azure using a Medallion Architecture (Bronze, Silver, Gold). The pipeline extracts data from PostgreSQL, ingests it into Azure Data Lake Storage Gen2 using Azure Data Factory, transforms it using Azure Databricks with Delta Lake, performs Incremental Loading and Slowly Changing Dimension (SCD Type 2), exposes curated business data through Azure Synapse Serverless SQL, and finally visualizes the data using Power BI.

The project simulates a real-world retail analytics solution capable of handling incremental data ingestion, historical tracking, scalable data transformations, and business intelligence reporting.

---

# 🏗️ Architecture

```
PostgreSQL
      │
      ▼
Azure Data Factory
(Incremental Load + Watermark)
      │
      ▼
Azure Data Lake Storage Gen2
Bronze Layer
      │
      ▼
Azure Databricks
(Data Cleaning & Delta Lake)
      │
      ▼
Silver Layer
      │
      ▼
SCD Type 2 + Business Transformations
      │
      ▼
Gold Layer
      │
      ▼
Azure Synapse Serverless SQL
      │
      ▼
Power BI Dashboard
```

---

# 🛠️ Technologies Used

- Microsoft Azure
- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- Apache Spark (PySpark)
- Delta Lake
- Azure Synapse Analytics
- PostgreSQL
- SQL
- Power BI
- Git & GitHub

---

# 📂 Dataset

The project contains the following retail datasets:

- Customers
- Products
- Orders
- Order Items

Approximately:

- 10,000 Customers
- 5,000 Products
- 100,000 Orders
- 300,000+ Order Items

---

# Bronze Layer

The Bronze layer stores raw source data exactly as received from PostgreSQL.

Features:

- Incremental ingestion
- Watermark implementation
- Dynamic folder creation
- Load Date partitioning
- Raw CSV storage

Azure Data Factory is responsible for loading incremental data from PostgreSQL into ADLS Gen2 Bronze.

---

# Silver Layer

The Silver layer performs data cleaning and standardization.

Transformations include:

- Removing duplicate records
- Null value validation
- Data type conversion
- Timestamp conversion
- Data quality checks
- Delta Lake storage
- Incremental MERGE operations

The Silver layer stores data in Delta format.

---

# Incremental Loading

Incremental loading is implemented using:

- Watermark Table
- Lookup Activity
- Copy Activity
- Dynamic Parameters
- MERGE INTO

Only newly inserted or updated records are processed, significantly reducing processing time.

---

# Slowly Changing Dimension (SCD Type 2)

Customer and Product dimensions support historical tracking.

Columns used:

- effective_date
- end_date
- is_current

Whenever a customer or product attribute changes:

- Previous record is expired
- New version is inserted
- Full history is preserved

---

# Gold Layer

The Gold layer contains business-ready dimensional models.

Tables:

- dim_customers
- dim_products
- dim_date
- fact_sales

Gold tables are optimized for reporting and analytics.

---

# Star Schema

The warehouse follows a Star Schema design.

Dimensions:

- Customer
- Product
- Date

Fact Table:

- Sales

Surrogate keys are generated for dimension tables to improve performance and support SCD Type 2.

---

# Azure Synapse Analytics

Azure Synapse Serverless SQL is used to expose Gold Delta tables through SQL views.

Benefits:

- No data duplication
- Direct querying of Delta files
- Serverless architecture
- Lower cost
- Easy Power BI integration

Views created:

- vw_dim_customers
- vw_dim_products
- vw_dim_date
- vw_fact_sales

---

# Power BI

Power BI connects directly to Azure Synapse Serverless SQL.

Dashboard includes:

- Executive Dashboard
- Customer Analytics
- Product Analytics
- Sales Analytics
- Order Analytics

KPIs include:

- Total Sales
- Total Orders
- Total Customers
- Total Products
- Revenue by Category
- Monthly Sales Trend
- Top Customers
- Sales by State

---

# Data Engineering Features

✔ Incremental Loading

✔ Watermarking

✔ Delta Lake

✔ Delta MERGE

✔ Slowly Changing Dimension Type 2

✔ Medallion Architecture

✔ Star Schema

✔ Azure Synapse Serverless SQL

✔ Power BI Reporting

---

# Project Workflow

1. Load data from PostgreSQL.
2. Azure Data Factory performs incremental ingestion.
3. Raw data lands in Bronze.
4. Databricks cleans and validates data.
5. Silver Delta tables are created.
6. Incremental MERGE updates Silver.
7. SCD Type 2 tracks historical changes.
8. Gold dimensional model is generated.
9. Synapse exposes Gold through SQL views.
10. Power BI consumes Synapse views for analytics.

---

# Repository Structure

```
Azure-Retail-Data-Engineering-Project
│
├── adf
├── architecture
├── databricks
├── docs
├── powerbi
├── screenshots
├── sql
├── synapse
└── README.md
```

---

# Future Enhancements

- CI/CD using Azure DevOps
- Azure Key Vault integration
- Data Quality Framework
- Monitoring using Azure Monitor
- Incremental Refresh in Power BI
- Row-Level Security (RLS)
- Microsoft Fabric Migration

---

# Learning Outcomes

This project demonstrates practical experience with:

- Cloud Data Engineering
- Data Lake Architecture
- Azure Services
- ETL Pipeline Development
- Incremental Processing
- Delta Lake
- Data Warehousing
- SQL Analytics
- Business Intelligence
- End-to-End Analytics Pipeline

---

# Author

**Salman Shaikh**

Azure Data Engineer | Data Analyst



---

⭐ If you found this project useful, consider giving it a star.
