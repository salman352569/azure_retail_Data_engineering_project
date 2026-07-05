CREATE Database Retail_DW;
Go
SELECT name 
From sys.databases;
-- using database
USE Retail_DW;
GO
-- CREATE A MASTER KEY 
CREATE MASTER KEY ENCRYPTION BY PASSWORD ='Saluu@12345678';
GO
--CREATE DATABASE SCOPED CREDENTIALS 
CREATE DATABASE SCOPED CREDENTIAL SynapseManagedIdentity
WITH IDENTITY ='Managed Identity';
GO

Drop External Data source GoldStorage;
-- CREATE EXTERNAL DATA SOURCE 
CREATE EXTERNAL DATA SOURCE GoldStorage
WITH
(
    LOCATION='https://retailstorage352.dfs.core.windows.net',
    CREDENTIAL=SynapseManagedIdentity
)


-- Test reading data for customers 
SELECT TOP 10 * FROM 
OPENROWSET(
    BULK'gold/dim_customers',
    DATA_SOURCE='GoldStorage',
    FORMAT='Delta'
)As rows ;


-- Test reading data for products 
SELECT TOP 10 * FROM 
OPENROWSET(
    BULK'gold/dim_products',
    DATA_SOURCE='GoldStorage',
    FORMAT='delta'
)AS rows ;

-- CREATING VIEWS 
CREATE VIEW vw_dim_customers
AS 
SELECT * FROM 
OPENROWSET(
    BULK 'gold/dim_customers',
    DATA_SOURCE='GoldStorage',
    FORMAT='delta'
) As Rows 
GO




-- Top 10 customers by revenue
SELECT  TOP 10
        c.customer_name,
        sum(f.sales_amount) AS total_sales
FROM  vw_fact_sales f
JOIN  vw_dim_customers c 
ON  c.customer_key = f.customer_key
group by c.customer_name
order by total_sales DESC;  


-- sales by category 
SELECT 
       p.category,
       sum(f.sales_amount) AS Revenue
FROM vw_fact_sales f 
join vw_dim_products p 
ON f.product_key = p.product_key
group by category 
order by Revenue DESC;

--Monthly sales
SELECT 
      d.year,
      d.month_name,
      sum(f.sales_amount) as Rvenue_by_month
FROM vw_fact_sales  f
join vw_dim_date d
ON f.date_key = d.date_key
GROUP BY d.year,d.month_name
ORDER BY d.year,MIN(d.month);
