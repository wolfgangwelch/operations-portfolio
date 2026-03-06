# Raw Data Inputs

This directory contains the operational data inputs used by the Inventory Command Center pipeline.

These files simulate real nightlife venue operational data such as vendor purchases, bar transfers, POS sales, and cocktail recipes.

The Python ETL loaders inside `src/` ingest these files and normalize them into the PostgreSQL database.

---

## purchases.csv

Records vendor liquor purchases.

Example structure:

venue_id,purchase_date,vendor_name,product_name,purchase_unit,quantity,unit_cost

Field descriptions:

- **venue_id** — venue receiving the purchase
- **purchase_date** — date of delivery
- **vendor_name** — distributor name
- **product_name** — product being purchased
- **purchase_unit** — `case` or `bottle`
- **quantity** — number of units purchased
- **unit_cost** — cost per unit

---

## transfers.csv

Tracks internal inventory movement.

Transfers can occur:

- between bars within a venue
- between storage and bars
- between venues

Example structure:

transfer_date,product_name,from_venue,from_location,to_venue,to_location,quantity,manager,notes

Field descriptions:

- **transfer_date** — date of transfer
- **product_name** — product moved
- **from_venue / from_location** — origin
- **to_venue / to_location** — destination
- **quantity** — number of bottles moved
- **manager** — manager approving transfer
- **notes** — optional explanation

---

## pos_sales.csv

Simulated point-of-sale transactions used to estimate theoretical liquor depletion.

Example structure:

venue_id,sale_date,item_name,sale_type,quantity

Field descriptions:

- **venue_id** — venue where sale occurred
- **sale_date** — transaction date
- **item_name** — cocktail or shot name
- **sale_type** — `cocktail` or `shot`
- **quantity** — number of drinks sold

---

## recipes.csv

Defines cocktail recipes used to calculate theoretical liquor usage.

Example structure:

drink_name,product_name,ounces_per_drink

Field descriptions:

- **drink_name** — cocktail name
- **product_name** — liquor used
- **ounces_per_drink** — amount used in each drink

---

## Why This Matters

These files simulate the operational data environment of a multi-venue nightlife group.

They allow the system to demonstrate:

- purchase normalization
- bottle-level depletion
- inventory variance detection
- theoretical liquor usage
- demand forecasting
