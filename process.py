import os
import json
import csv

RAW_DIR = "main/raw-data"
OUTPUT_JSON_DIR = "output/output-json"
OUTPUT_CSV = "output/output-data.csv"

os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

all_data = []
data_by_region = {}

# Baca semua file JSON mentah
for fname in os.listdir(RAW_DIR):
    if fname.endswith(".json"):
        with open(os.path.join(RAW_DIR, fname)) as f:
            data = json.load(f)
            region = data.get("city") or data.get("regency") or "unknown"
            # Anggap data adalah list, jika tidak, sesuaikan struktur di sini
            if isinstance(data, list):
                data_by_region.setdefault(region, []).extend(data)
                all_data.extend(data)
            else:
                data_by_region.setdefault(region, []).append(data)
                all_data.append(data)

# Output per kabupaten/kota
for region, items in data_by_region.items():
    slug = region.lower().replace(" ", "_")
    with open(f"{OUTPUT_JSON_DIR}/{slug}.json", "w") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

# Output CSV
with open(OUTPUT_CSV, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "place_id", "city"])
    for item in all_data:
        writer.writerow([
            item.get("name"),
            item.get("place_id") or item.get("placeId"),
            item.get("city") or item.get("regency")
        ])
