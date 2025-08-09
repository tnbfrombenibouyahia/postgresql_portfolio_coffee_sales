-- revenue_by_region.sql
SELECT st.region AS label,
       SUM(s.quantity * p.price) AS value
FROM sales s
JOIN stores st USING (store_id)
JOIN products p USING (product_id)
GROUP BY st.region
ORDER BY value DESC;
