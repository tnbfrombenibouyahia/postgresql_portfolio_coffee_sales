-- top_products_by_gross_margin.sql
SELECT p.product_name AS label,
       SUM(s.quantity * (p.price - p.cost)) AS value
FROM sales s
JOIN products p USING (product_id)
GROUP BY p.product_name
ORDER BY value DESC
LIMIT 5;
