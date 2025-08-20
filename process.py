import os, json, csv
from collections import defaultdict

INPUT_FOLDER = "raw-data"
OUTPUT_FOLDER = "output-json"
CSV_FILE = "output-data.csv"

if not os.path.isdir(INPUT_FOLDER):
    raise FileNotFoundError(f"Folder {INPUT_FOLDER} tidak ditemukan. Pastikan ada di repo.")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Gabung semua JSON mentah
all_records = []
for fn in os.listdir(INPUT_FOLDER):
    if fn.endswith(".json"):
        with open(os.path.join(INPUT_FOLDER, fn), encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_records.extend(data)
            except Exception as e:
                print(f"[!] Error baca {fn}: {e}")

print("Total records mentah:", len(all_records))

# Dedup berdasarkan place_id
deduped = {}
for rec in all_records:
    pid = rec.get("place_id")
    if not pid: 
        continue
    if pid not in deduped:
        deduped[pid] = rec
    else:
        for k, v in rec.items():
            if k not in deduped[pid] or not deduped[pid][k]:
                deduped[pid][k] = v

all_records = list(deduped.values())
print("Setelah dedup:", len(all_records))

# Split per kabupaten/kota
groups = defaultdict(list)
for rec in all_records:
    city = rec.get("city") or rec.get("state") or "lainnya"
    groups[city].append(rec)

# Simpan JSON per kabupaten
for city, items in groups.items():
    safe_name = city.lower().replace(" ", "_").replace("/", "-")
    outpath = os.path.join(OUTPUT_FOLDER, f"{safe_name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"[OK] {outpath} : {len(items)} entri")

# Buat CSV ringkas (untuk knowledge)
with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "place_id", "city"])
    for city in sorted(groups.keys()):
        for rec in groups[city]:
            writer.writerow([rec.get("title") or rec.get("name"), rec.get("place_id"), city])

print("[OK] CSV dibuat:", CSV_FILE)
