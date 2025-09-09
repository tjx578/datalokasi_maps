# Datalokasi Maps API

API endpoint untuk mengakses data lokasi maps Indonesia yang dapat digunakan oleh Custom GPT Navi Pro.

## Base URL
```
https://tjx578.github.io/datalokasi_maps
```

## Endpoints

### 1. API Information
```
GET /api/v1/index.json
```
Mendapatkan informasi dasar API dan statistik data.

**Response:**
```json
{
  "name": "Datalokasi Maps API",
  "version": "1.0.0",
  "total_records": 6918,
  "total_cities": 306,
  "last_updated": "2025-09-09T01:54:57.155637Z"
}
```

### 2. All Data
```
GET /api/v1/data.json
```
Mendapatkan semua data lokasi dalam format JSON.

### 3. CSV Export
```
GET /api/v1/data.csv
```
Mendapatkan semua data dalam format CSV.

### 4. Cities List
```
GET /api/v1/cities.json
```
Mendapatkan daftar kota/wilayah yang tersedia.

**Response:**
```json
{
  "gianyar_regency": {
    "count": 1307,
    "endpoint": "/api/v1/regions/gianyar_regency.json"
  },
  "denpasar_city": {
    "count": 1213,
    "endpoint": "/api/v1/regions/denpasar_city.json"
  }
}
```

### 5. Regional Data
```
GET /api/v1/regions/{city_name}.json
```
Mendapatkan data lokasi untuk kota/wilayah tertentu.

**Parameters:**
- `city_name`: Nama kota (contoh: `gianyar_regency`, `denpasar_city`)

## Contoh Usage untuk Custom GPT

### Mengambil semua data
```javascript
fetch('https://tjx578.github.io/datalokasi_maps/api/v1/data.json')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Mengambil data untuk kota tertentu
```javascript
fetch('https://tjx578.github.io/datalokasi_maps/api/v1/regions/gianyar_regency.json')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Mendapatkan daftar kota
```javascript
fetch('https://tjx578.github.io/datalokasi_maps/api/v1/cities.json')
  .then(response => response.json())
  .then(cities => {
    Object.keys(cities).forEach(city => {
      console.log(`${city}: ${cities[city].count} locations`);
    });
  });
```

## Data Schema

Setiap lokasi memiliki struktur data:

```json
{
  "title": "Nama lokasi",
  "place_id": "Google Place ID",
  "address": "Alamat lengkap",
  "city": "Kota/Kabupaten",
  "state": "Provinsi",
  "country": "Negara",
  "gps_coordinates": {
    "latitude": -8.5368389,
    "longitude": 115.41486479999999
  },
  "type": "Kategori lokasi",
  "rating": 5.0,
  "reviews": 10
}
```

## Kota/Wilayah Terbesar

Berdasarkan jumlah lokasi:
1. **Gianyar Regency**: 1,307 lokasi
2. **Denpasar City**: 1,213 lokasi  
3. **Jembrana Regency**: 825 lokasi
4. **Tabanan Regency**: 814 lokasi
5. **Badung Regency**: 740 lokasi

## CORS

API ini mendukung CORS untuk akses dari browser dan aplikasi web.

## Rate Limiting

Tidak ada rate limiting - data di-host sebagai file statis di GitHub Pages.

## OpenAPI Schema

Schema OpenAPI tersedia di: `/api/v1/schema.json`