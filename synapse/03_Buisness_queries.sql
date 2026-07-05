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
