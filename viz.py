# generate_charts.py
# Generate 5 PNG charts from PostgreSQL for your README, with coffee-themed styling.

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# ---------- DB config ----------
DB = dict(
    dbname="coffee_sales",
    user="postgres",
    password="Makarov33!",     # <- change if needed
    host="localhost",
    port=5432,
)

# ---------- Output folder ----------
OUT = Path("images")
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Coffee palette ----------
COFFEE      = "#6F4E37"  # main coffee brown
COFFEE_DARK = "#4B3621"  # darker roast
COFFEE_LIGHT= "#A9745B"  # latte

plt.rcParams.update({
    "axes.edgecolor": COFFEE_DARK,
    "axes.titleweight": "bold",
    "xtick.color": COFFEE_DARK,
    "ytick.color": COFFEE_DARK,
    "text.color": COFFEE_DARK,
    "axes.labelcolor": COFFEE_DARK,
})

# ---------- Queries ----------
QUERIES = {
    # 1) Revenue by product
    "revenue_by_product": """
        SELECT p.product_name AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY p.product_name
        ORDER BY value DESC;
    """,
    # 2) Gross margin by category
    "gross_margin_by_category": """
        SELECT p.category AS label,
               SUM(s.quantity * (p.price - p.cost)) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY p.category
        ORDER BY value DESC;
    """,
    # 3) Revenue by region
    "revenue_by_region": """
        SELECT st.region AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN stores st USING (store_id)
        JOIN products p USING (product_id)
        GROUP BY st.region
        ORDER BY value DESC;
    """,
    # 4) Monthly revenue (trend)
    "monthly_revenue": """
        SELECT DATE_TRUNC('month', s.sale_date) AS label,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY label
        ORDER BY label;
    """,
    # 5) NEW: Revenue by day of week (Mon..Sun)
    "revenue_by_dow": """
        SELECT TO_CHAR(s.sale_date, 'Dy') AS label,
               EXTRACT(ISODOW FROM s.sale_date) AS dow_num,
               SUM(s.quantity * p.price) AS value
        FROM sales s
        JOIN products p USING (product_id)
        GROUP BY label, dow_num
        ORDER BY dow_num;
    """,
}

# ---------- Plot helpers ----------
def _decorate_axes(title: str):
    plt.title(title)
    plt.xlabel("")
    plt.ylabel("")
    plt.grid(axis="y", alpha=0.25, linestyle="--")

def save_bar(df: pd.DataFrame, title: str, filename: str, horizontal=False):
    plt.figure()
    if horizontal:
        ax = df.plot(kind="barh", x="label", y="value", legend=False,
                     color=COFFEE, edgecolor=COFFEE_DARK, linewidth=0.6)
        ax.invert_yaxis()
    else:
        ax = df.plot(kind="bar", x="label", y="value", legend=False,
                     color=COFFEE, edgecolor=COFFEE_DARK, linewidth=0.6)
        plt.xticks(rotation=45, ha="right")
    _decorate_axes(title)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

def save_line(df: pd.DataFrame, title: str, filename: str, is_month=False):
    plt.figure()
    if is_month:
        # nice YYYY-MM format on x-axis
        df = df.copy()
        df["label"] = pd.to_datetime(df["label"]).dt.to_period("M").astype(str)
    df = df.sort_values("label")
    df.plot(x="label", y="value", legend=False, marker="o",
            color=COFFEE_DARK, linewidth=2, markersize=6)
    plt.xticks(rotation=45, ha="right")
    _decorate_axes(title)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

# ---------- Main ----------
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
            save_line(df, "Monthly Revenue (€)", "monthly_revenue.png", is_month=True)

        elif key == "revenue_by_dow":
            # ensure correct Mon..Sun order using the dow_num we selected
            df = df.sort_values("dow_num")[["label", "value"]]
            save_bar(df, "Revenue by Day of Week (€)", "revenue_by_dow.png")

    conn.close()
    print(f"✅ Charts saved to: {OUT.resolve()}")

if __name__ == "__main__":
    main()
