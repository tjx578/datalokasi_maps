import os
import json
import csv
from collections import defaultdict

INPUT_FOLDER = "raw-data"
OUTPUT_FOLDER = "output-json"
CSV_FILE = "output-data.csv"

# --- 1. Validasi folder input ---
if not os.path.isdir(INPUT_FOLDER):
    raise FileNotFoundError(
        f"Folder '{INPUT_FOLDER}' tidak ditemukan. "
        f"Pastikan Anda membuat folder dan meletakkan file JSON mentah di sana."
    )

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- 2. Gabungkan semua JSON mentah ---
all_records = []
for fn in os.listdir(INPUT_FOLDER):
    if fn.endswith(".json"):
        path = os.path.join(INPUT_FOLDER, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_records.extend(data)
                else:
                    print(f"[!] Lewati {fn}: bukan array JSON")
        except Exception as e:
            print(f"[!] Error membaca {fn}: {e}")

print("Total records mentah:", len(all_records))

# --- 3. Dedup berdasarkan place_id ---
deduped = {}
for rec in all_records:
    pid = rec.get("place_id")
    if not pid:
        continue
    if pid not in deduped:
        deduped[pid] = rec
    else:
        # Gabungkan jika ada data tambahan
        for k, v in rec.items():
            if k not in deduped[pid] or not deduped[pid][k]:
                deduped[pid][k] = v

all_records = list(deduped.values())
print("Setelah dedup:", len(all_records))

# --- 4. Kelompokkan berdasarkan city/state ---
groups = defaultdict(list)
for rec in all_records:
    city = rec.get("city") or rec.get("state") or "lainnya"
    groups[city].append(rec)

# --- 5. Simpan JSON per kabupaten/kota ---
for city, items in groups.items():
    safe_name = city.lower().replace(" ", "_").replace("/", "-")
    outpath = os.path.join(OUTPUT_FOLDER, f"{safe_name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"[OK] {outpath} : {len(items)} entri")

# --- 6. Buat CSV ringkas (name, place_id, city) ---
with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "place_id", "city"])
    for city in sorted(groups.keys()):
        for rec in groups[city]:
            writer.writerow([
                rec.get("title") or rec.get("name"),
                rec.get("place_id"),
                city
            ])

print("[OK] CSV dibuat:", CSV_FILE)

