from db_connection import get_cursor

VENUES = [
    (1, "Gold Club", True),
    (2, "Condor", True),
    (3, "Hustler Club", True),
    (4, "Penthouse", True),
    (5, "Garden of Eden", False),
    (6, "Little Darlings", False),
    (7, "Hungry Eye", True),
    (8, "Centerfolds", False),
    (9, "New Century", False),
]

LOCATIONS = [
    (1, 1, "Main Bar"),
    (2, 1, "VIP Bar"),
    (3, 1, "Storage"),
    (4, 2, "Bar"),
    (5, 2, "Storage"),
    (6, 3, "Bar"),
    (7, 3, "Storage"),
    (8, 4, "Main Bar"),
    (9, 4, "VIP Bar"),
    (10, 4, "Storage"),
    (11, 5, "Bar"),
    (12, 5, "Storage"),
    (13, 6, "Bar"),
    (14, 6, "Storage"),
    (15, 7, "Bar"),
    (16, 7, "Storage"),
    (17, 8, "Bar"),
    (18, 8, "Storage"),
    (19, 9, "Bar"),
    (20, 9, "Storage"),
]

SHOT_CATEGORIES = [
    ("Vodka", 2.0),
    ("Tequila", 2.0),
    ("Whiskey", 2.0),
    ("Cognac", 2.0),
    ("Rum", 2.0),
    ("Gin", 2.0),
]


def seed_venues():
    with get_cursor(commit=True) as (_, cur):
        cur.executemany(
            """
            INSERT INTO venues (venue_id, venue_name, liquor_license)
            VALUES (%s, %s, %s)
            ON CONFLICT (venue_id) DO NOTHING;
            """,
            VENUES,
        )
    print("Seeded venues.")


def seed_locations():
    with get_cursor(commit=True) as (_, cur):
        cur.executemany(
            """
            INSERT INTO locations (location_id, venue_id, location_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (location_id) DO NOTHING;
            """,
            LOCATIONS,
        )
    print("Seeded locations.")


def seed_shot_categories():
    with get_cursor(commit=True) as (_, cur):
        cur.executemany(
            """
            INSERT INTO shot_categories (category_name, ounces_per_shot)
            VALUES (%s, %s)
            ON CONFLICT (category_name) DO NOTHING;
            """,
            SHOT_CATEGORIES,
        )
    print("Seeded shot categories.")


if __name__ == "__main__":
    seed_venues()
    seed_locations()
    seed_shot_categories()
