-- monthly_revenue.sql
SELECT DATE_TRUNC('month', s.sale_date) AS label,
       SUM(s.quantity * p.price) AS value
FROM sales s
JOIN products p USING (product_id)
GROUP BY label
ORDER BY label;
