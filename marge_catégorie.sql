-- gross_margin_by_category.sql
SELECT p.category AS label,
       SUM(s.quantity * (p.price - p.cost)) AS value
FROM sales s
JOIN products p USING (product_id)
GROUP BY p.category
ORDER BY value DESC;
