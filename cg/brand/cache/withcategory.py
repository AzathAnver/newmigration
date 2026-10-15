import json
import csv

# Load JSON file
with open("hierarchy_cache.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# Loop through all items
for item_id, item in data.items():
    if item.get("type") == "CLIENT":
        client_name = item.get("name")

        # Get MARKET IDs
        for market_id in item.get("children", []):
            market = data.get(market_id)

            if not market or market.get("type") != "MARKET":
                continue

            market_name = market.get("name")

            # Get BRAND IDs
            for brand_id in market.get("children", []):
                brand = data.get(brand_id)

                if not brand or brand.get("type") != "BRAND":
                    continue

                brand_name = brand.get("name")

                # Get category name
                categories = brand.get("categories", [])
                category_name = categories[0].get("name") if categories else ""

                # Add row
                rows.append([
                    client_name,
                    market_name,
                    brand_name,
                    category_name
                ])

# Write to CSV
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Header
    writer.writerow(["Client", "Market", "Brand", "Category"])

    writer.writerows(rows)

print("CSV generated successfully!")
