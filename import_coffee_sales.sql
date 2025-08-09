COPY stores (store_id, store_name, city, region, open_date)
FROM '/Users/theonaimbenhellal/Desktop/Stores Projet SQL.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COPY products (product_id, product_name, category, price, cost)
FROM '/Users/theonaimbenhellal/Desktop/Produits Projet SQL.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COPY customers (customer_id, first_name, last_name, gender, birth_date)
FROM '/Users/theonaimbenhellal/Desktop/Clients Projet SQL.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

COPY sales (sale_id, store_id, product_id, customer_id, sale_date, quantity)
FROM '/Users/theonaimbenhellal/Desktop/Ventes Projet SQL.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
