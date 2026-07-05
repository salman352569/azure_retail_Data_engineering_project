-- CREATING VIEWS 
-- Dim Customers 
CREATE VIEW vw_dim_customers
AS 
SELECT * FROM 
OPENROWSET(
    BULK 'gold/dim_customers',
    DATA_SOURCE='GoldStorage',
    FORMAT='delta'
) As Rows 
GO
--Dim Products
CREATE VIEW vw_dim_products
AS 
SELECT * FROM 
OPENROWSET(
    BULK 'gold/dim_products',
    DATA_SOURCE='GoldStorage',
    FORMAT='delta'
) As Rows 
GO
-- date 
CREATE VIEW vw_dim_date
AS
SELECT *
FROM OPENROWSET(
    BULK 'gold/dim_date',
    DATA_SOURCE = 'GoldStorage',
    FORMAT = 'DELTA'
) AS rows;
GO

CREATE VIEW vw_fact_sales
AS 
SELECT * FROM 
OPENROWSET(
    BULK 'gold/Fact_sales',
    DATA_SOURCE='GoldStorage',
    FORMAT='delta'
) As Rows 
GO