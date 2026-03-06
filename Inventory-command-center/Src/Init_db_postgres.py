from db_connection import get_cursor


DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS venues (
        venue_id INTEGER PRIMARY KEY,
        venue_name TEXT NOT NULL UNIQUE,
        liquor_license BOOLEAN NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY,
        venue_id INTEGER NOT NULL REFERENCES venues(venue_id),
        location_name TEXT NOT NULL,
        UNIQUE (venue_id, location_name)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id SERIAL PRIMARY KEY,
        vendor_name TEXT NOT NULL UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        alcoholic BOOLEAN NOT NULL,
        bottle_ml INTEGER,
        ounces_per_bottle REAL,
        default_pour_oz REAL,
        case_size INTEGER,
        par_level REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id SERIAL PRIMARY KEY,
        venue_id INTEGER NOT NULL REFERENCES venues(venue_id),
        purchase_date DATE NOT NULL,
        vendor_id INTEGER REFERENCES vendors(vendor_id),
        product_id INTEGER NOT NULL REFERENCES products(product_id),
        purchase_unit TEXT NOT NULL CHECK (purchase_unit IN ('case', 'bottle')),
        quantity REAL NOT NULL CHECK (quantity >= 0),
        unit_cost REAL NOT NULL CHECK (unit_cost >= 0),
        bottle_quantity REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS transfers (
        transfer_id SERIAL PRIMARY KEY,
        transfer_date DATE NOT NULL,
        product_id INTEGER NOT NULL REFERENCES products(product_id),
        from_venue INTEGER NOT NULL REFERENCES venues(venue_id),
        from_location INTEGER NOT NULL REFERENCES locations(location_id),
        to_venue INTEGER NOT NULL REFERENCES venues(venue_id),
        to_location INTEGER NOT NULL REFERENCES locations(location_id),
        quantity REAL NOT NULL CHECK (quantity >= 0),
        manager TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS inventory_counts (
        count_id SERIAL PRIMARY KEY,
        venue_id INTEGER NOT NULL REFERENCES venues(venue_id),
        location_id INTEGER NOT NULL REFERENCES locations(location_id),
        product_id INTEGER NOT NULL REFERENCES products(product_id),
        count_date DATE NOT NULL,
        quantity REAL NOT NULL CHECK (quantity >= 0),
        count_type TEXT NOT NULL CHECK (count_type IN ('weekly', 'audit')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id SERIAL PRIMARY KEY,
        drink_name TEXT NOT NULL,
        product_id INTEGER NOT NULL REFERENCES products(product_id),
        ounces_per_drink REAL NOT NULL CHECK (ounces_per_drink > 0),
        UNIQUE (drink_name, product_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS shot_categories (
        shot_category_id SERIAL PRIMARY KEY,
        category_name TEXT NOT NULL UNIQUE,
        ounces_per_shot REAL NOT NULL CHECK (ounces_per_shot > 0)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS pos_sales (
        sale_id SERIAL PRIMARY KEY,
        venue_id INTEGER NOT NULL REFERENCES venues(venue_id),
        sale_date DATE NOT NULL,
        item_name TEXT NOT NULL,
        sale_type TEXT NOT NULL CHECK (sale_type IN ('cocktail', 'shot')),
        quantity INTEGER NOT NULL CHECK (quantity >= 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
]


def create_tables():
    with get_cursor(commit=True) as (_, cur):
        for ddl in DDL_STATEMENTS:
            cur.execute(ddl)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()
