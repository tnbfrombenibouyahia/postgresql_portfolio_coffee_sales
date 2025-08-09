-- revenue_by_product.sql
SELECT p.product_name AS label,
       SUM(s.quantity * p.price) AS value
FROM sales s
JOIN products p USING (product_id)
GROUP BY p.product_name
ORDER BY value DESC;
