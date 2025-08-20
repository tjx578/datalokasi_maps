# Instruksi Workflow Data CI untuk Repo Public

Gunakan contoh workflow YAML berikut untuk repo publik **tanpa** menggunakan Personal Access Token (PAT) dan **tanpa** melakukan `npm install`. Workflow ini melakukan pengecekan file JSON dan GeoJSON dengan `jq` pada repo sendiri maupun dapat mengakses repo publik lain.

```yaml
name: Data CI

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout this repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Jika perlu menarik repo public lain (opsional)
      - name: Checkout datalokasi_maps (public)
        uses: actions/checkout@v4
        with:
          repository: tjx578/datalokasi_maps
          path: datalokasi_maps
          fetch-depth: 0

      - name: List files
        run: |
          ls -R
          ls -R datalokasi_maps || true

      - name: Validate JSON
        run: |
          set -e
          shopt -s globstar nullglob
          for f in datalokasi_maps/**/*.json; do
            echo "checking $f"
            jq -e . "$f" >/dev/null
          done

      - name: Validate GeoJSON
        run: |
          set -e
          shopt -s globstar nullglob
          for f in datalokasi_maps/**/*.geojson; do
            echo "checking $f"
            jq -e . "$f" >/dev/null
          done
```

## Catatan

- **Repo public tidak perlu token khusus**: Aksi ini berjalan tanpa PAT/GITHUB_TOKEN tambahan, cukup gunakan workflow seperti di atas.
- **Hapus langkah "Checkout datalokasi_maps"** jika workflow ini dijalankan di repo `datalokasi_maps` itu sendiri.
- Pastikan dependensi `jq` sudah tersedia di runner (default di Ubuntu runner GitHub Actions).
- Langkah “List files” opsional, berguna untuk debug.

---
Workflow ini cocok untuk memvalidasi data JSON & GeoJSON pada repo publik secara otomatis di GitHub Actions.
