# generate_charts.py
# Génère 5 graphiques (PNG) depuis PostgreSQL pour le README.

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from pathlib import Path

# ---------- Config ----------
DB = dict(
    dbname="coffee_sales",
    user="postgres",
    password="Makarov33!",   # <- adapte si besoin
    host="localhost",
    port=5432,
)

OUT = Path("images")
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = {
    # 1) CA par produit (bar)
    "revenue_by_product": """
        SELECT p.product_name AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY p.product_name
        ORDER BY value DESC;
    """,
    # 2) Marge brute par catégorie (bar)
    "gross_margin_by_category": """
        SELECT p.category AS label,
               SUM(s.quantity * (p.price - p.cost)) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY p.category
        ORDER BY value DESC;
    """,
    # 3) CA par région (bar)
    "revenue_by_region": """
        SELECT st.region AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN stores st USING (store_id)
        JOIN products p USING (product_id)
        GROUP BY st.region
        ORDER BY value DESC;
    """,
    # 4) Tendance mensuelle du CA (line)
    "monthly_revenue": """
        SELECT DATE_TRUNC('month', s.sale_date) AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY label
        ORDER BY label;
    """,
    # 5) Top 5 produits par marge brute (bar horizontal)
    "top_products_by_gross_margin": """
        SELECT p.product_name AS label,
               SUM(s.quantity * (p.price - p.cost)) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY p.product_name
        ORDER BY value DESC
        LIMIT 5;
    """,
}

def save_bar(df: pd.DataFrame, title: str, filename: str, horizontal=False):
    plt.figure()
    if horizontal:
        df.plot(kind="barh", x="label", y="value", legend=False)
        plt.gca().invert_yaxis()
    else:
        df.plot(kind="bar", x="label", y="value", legend=False)
        plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

def save_line(df: pd.DataFrame, title: str, filename: str):
    plt.figure()
    df = df.sort_values("label")
    df.plot(x="label", y="value", legend=False, marker="o")
    plt.title(title)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

def main():
    conn = psycopg2.connect(**DB)
    for key, sql in QUERIES.items():
        df = pd.read_sql(sql, conn)

        if key == "revenue_by_product":
            save_bar(df, "Revenue by Product (€)", "revenue_by_product.png")
        elif key == "gross_margin_by_category":
            save_bar(df, "Gross Margin by Category (€)", "gross_margin_by_category.png")
        elif key == "revenue_by_region":
            save_bar(df, "Revenue by Region (€)", "revenue_by_region.png")
        elif key == "monthly_revenue":
            save_line(df, "Monthly Revenue (€)", "monthly_revenue.png")
        elif key == "top_products_by_gross_margin":
            save_bar(df, "Top 5 Products by Gross Margin (€)",
                     "top_products_by_gross_margin.png", horizontal=True)

    conn.close()
    print(f"✅ Charts saved to: {OUT.resolve()}")

if __name__ == "__main__":
    main()
