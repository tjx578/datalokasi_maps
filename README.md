lokasi-data

Pipeline otomatis (GitHub Actions) untuk:

Gabung + dedup (place_id)

Split JSON per kab/kota → output-json/*.json

Buat CSV besar (name, place_id, city) → output-data.csv

Struktur
main/
├─ raw-data/              # taruh JSON mentah di sini
│  └─ .gitkeep
└─ process.py

output/
├─ output-json/
│  ├─ gianyar_regency.json
│  ├─ denpasar_city.json
│  └─ ...
└─ output-data.csv

Cara pakai

Upload JSON mentah ke main/raw-data/ → commit & push ke main.

Actions jalan otomatis → hasil muncul di branch output.

Link Raw (untuk Custom GPT / publik):

JSON per kab/kota
https://raw.githubusercontent.com/tjx578/datalokasi_maps/output/output-json/gianyar_regency.json

CSV besar
https://raw.githubusercontent.com/tjx578/datalokasi_maps/output/output-data.csv
