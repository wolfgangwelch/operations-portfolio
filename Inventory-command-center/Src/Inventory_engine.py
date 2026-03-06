import pandas as pd

from db_connection import connect_db


def inventory_snapshot() -> pd.DataFrame:
    conn = connect_db()

    query = """
    SELECT
        v.venue_name,
        l.location_name,
        p.product_name,
        p.category,
        SUM(ic.quantity) AS quantity_on_hand
    FROM inventory_counts ic
    JOIN venues v ON ic.venue_id = v.venue_id
    JOIN locations l ON ic.location_id = l.location_id
    JOIN products p ON ic.product_id = p.product_id
    WHERE ic.count_date = (
        SELECT MAX(sub.count_date)
        FROM inventory_counts sub
        WHERE sub.venue_id = ic.venue_id
          AND sub.location_id = ic.location_id
          AND sub.product_id = ic.product_id
    )
    GROUP BY v.venue_name, l.location_name, p.product_name, p.category
    ORDER BY v.venue_name, l.location_name, p.product_name;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def inventory_value() -> pd.DataFrame:
    conn = connect_db()

    query = """
    WITH latest_counts AS (
        SELECT
            ic.venue_id,
            ic.location_id,
            ic.product_id,
            ic.quantity,
            ROW_NUMBER() OVER (
                PARTITION BY ic.venue_id, ic.location_id, ic.product_id
                ORDER BY ic.count_date DESC
            ) AS rn
        FROM inventory_counts ic
    ),
    avg_costs AS (
        SELECT
            product_id,
            AVG(unit_cost) AS avg_unit_cost
        FROM purchases
        GROUP BY product_id
    )
    SELECT
        v.venue_name,
        l.location_name,
        p.product_name,
        lc.quantity,
        COALESCE(ac.avg_unit_cost, 0) AS avg_unit_cost,
        lc.quantity * COALESCE(ac.avg_unit_cost, 0) AS inventory_value
    FROM latest_counts lc
    JOIN venues v ON lc.venue_id = v.venue_id
    JOIN locations l ON lc.location_id = l.location_id
    JOIN products p ON lc.product_id = p.product_id
    LEFT JOIN avg_costs ac ON lc.product_id = ac.product_id
    WHERE lc.rn = 1
    ORDER BY v.venue_name, l.location_name, p.product_name;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def low_stock_alerts() -> pd.DataFrame:
    conn = connect_db()

    query = """
    WITH latest_counts AS (
        SELECT
            venue_id,
            product_id,
            quantity,
            ROW_NUMBER() OVER (
                PARTITION BY venue_id, product_id
                ORDER BY count_date DESC
            ) AS rn
        FROM inventory_counts
    )
    SELECT
        v.venue_name,
        p.product_name,
        p.par_level,
        lc.quantity
    FROM latest_counts lc
    JOIN venues v ON lc.venue_id = v.venue_id
    JOIN products p ON lc.product_id = p.product_id
    WHERE lc.rn = 1
      AND lc.quantity < p.par_level
    ORDER BY v.venue_name, p.product_name;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


if __name__ == "__main__":
    print(inventory_snapshot().head())
    print(inventory_value().head())
    print(low_stock_alerts().head())
