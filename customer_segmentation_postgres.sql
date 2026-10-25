CREATE TABLE online_retail (
    InvoiceNo VARCHAR(50),
    StockCode VARCHAR(50),
    Description TEXT,
    Quantity INT,
    InvoiceDate TIMESTAMP,
    UnitPrice NUMERIC,
    CustomerID FLOAT,
    Country VARCHAR(100),
    TotalPrice NUMERIC
);


CREATE TABLE customer_segments_1 (
    CustomerID FLOAT PRIMARY KEY,
    Recency INT,
    Frequency INT,
    Monetary NUMERIC,
	Cluster INT
);

SELECT*FROM online_retail;
SELECT*FROM customer_segments_1;

-- Total revenue 
SELECT SUM(TotalPrice) AS Total_Revenue FROM online_retail;  

-- Top 5 best selling products
SELECT Description, SUM(Quantity) AS Total_Quantity
FROM online_retail
GROUP BY Description
ORDER BY Total_Quantity DESC
LIMIT 5;   

-- Top 5 countries by sales 
SELECT Country, SUM(TotalPrice) AS Country_Sales
FROM online_retail
GROUP BY Country
ORDER BY Country_Sales DESC
LIMIT 5;   

-- Monthly sales trend 
SELECT DATE_TRUNC('month', InvoiceDate) AS Month, SUM(TotalPrice) AS Monthly_Sales
FROM online_retail
GROUP BY Month
ORDER BY Month;


-- Calculate summary statistics for each customer segment (Cluster)
-- This query shows the total number of customers, average spend, and total revenue per cluster
SELECT 
    Cluster,
    COUNT(CustomerID) AS Total_Customers,
    ROUND(AVG(Monetary), 2) AS Avg_Spend,
    ROUND(SUM(Monetary), 2) AS Total_Revenue_Generated
FROM customer_segments_1
GROUP BY Cluster
ORDER BY Total_Revenue_Generated DESC;

-- Retrieve top 10 highest spending customers from a specific cluster (e.g., VIP/Champions cluster)
SELECT * 
FROM customer_segments_1
WHERE Cluster = 3 -- (Note: Cluster ID may vary based on your clustering results)
ORDER BY Monetary DESC
LIMIT 10;

-- Find potential churn or at-risk customers who haven't made a purchase in over 30 days, ordered by highest spend
SELECT CustomerID, Recency, Frequency, Monetary
FROM customer_segments_1
WHERE Recency > 2 -- (Note: You can adjust the number of days based on your dataset)
ORDER BY Monetary DESC;
