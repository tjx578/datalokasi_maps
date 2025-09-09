# NaviPro Location Database

Sistem penyedia database lokasi maps untuk NaviPro melalui Replit. Repository ini memproses data lokasi mentah dan menyediakan API untuk akses data terstruktur.

## 🚀 Fitur Utama

- **Pemrosesan Data Otomatis**: Pipeline otomatis untuk mengolah data JSON mentah
- **API RESTful**: Endpoint untuk akses data lokasi
- **Interface Web**: Dashboard untuk monitoring dan pencarian
- **Integrasi Replit**: Siap deploy di Replit untuk akses NaviPro
- **Data Terstruktur**: Output JSON per region dan CSV lengkap

## 📁 Struktur Repository

```
datalokasi_maps/
├── main/                          # Folder utama proses data
│   ├── raw-data/                  # Data JSON mentah input
│   ├── output-json/               # Output JSON per region
│   ├── output-data.csv            # Output CSV lengkap  
│   └── process.py                 # Script pemroses data
├── api_server.py                  # Server API untuk NaviPro
├── templates/                     # Template web interface
├── requirements.txt               # Dependencies Python
├── .replit                        # Konfigurasi Replit
└── .github/workflows/process.yml  # GitHub Actions workflow
```

## 🔧 Setup dan Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/tjx578/datalokasi_maps.git
cd datalokasi_maps
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Proses Data (Opsional)
```bash
cd main
python process.py
```

### 4. Jalankan API Server
```bash
python api_server.py
```

## 🌐 API Endpoints

### Base URL
- Local: `http://localhost:5000`
- Replit: `https://your-repl-name.username.repl.co`

### Endpoints Tersedia

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Web interface dashboard |
| GET | `/api` | Informasi API |
| GET | `/health` | Status kesehatan server |
| GET | `/api/stats` | Statistik database |
| GET | `/api/regions` | Daftar semua region |
| GET | `/api/locations` | Semua lokasi (dengan pagination) |
| GET | `/api/locations/<city>` | Lokasi berdasarkan kota/kabupaten |
| GET | `/api/search?q=<query>` | Pencarian lokasi |

### Contoh Penggunaan API

```bash
# Mendapatkan statistik
curl http://localhost:5000/api/stats

# Pencarian lokasi
curl "http://localhost:5000/api/search?q=sekolah"

# Data lokasi Denpasar
curl http://localhost:5000/api/locations/denpasar_city
```

## 🔄 Workflow Otomatis

Repository ini menggunakan GitHub Actions untuk pemrosesan otomatis:

1. **Trigger**: Push ke branch `main` atau perubahan di `main/raw-data/`
2. **Proses**: Menjalankan `main/process.py`
3. **Output**: Menyimpan hasil ke `main/output-json/` dan `main/output-data.csv`

## 📊 Data yang Tersedia

Database mencakup lokasi dari berbagai kategori:
- Sekolah dan institusi pendidikan
- Tempat ibadah
- Fasilitas umum
- Bisnis dan komersial
- Dan kategori lainnya

### Coverage Geografis
- **Utama**: Bali (Denpasar, Gianyar, Badung, dll.)
- **Tambahan**: Jawa, Sumatra, dan wilayah Indonesia lainnya
- **Internasional**: Beberapa lokasi AS dan Eropa

## 🚀 Deploy di Replit

1. Import repository ke Replit
2. Install dependencies secara otomatis
3. Run `api_server.py`
4. API dapat diakses di URL Replit

### Konfigurasi Environment

```bash
# .env (opsional)
PORT=5000
PYTHONPATH=/home/runner/datalokasi_maps
```

## 🔌 Integrasi NaviPro

API ini dirancang untuk integrasi dengan NaviPro:

```javascript
// Contoh penggunaan di NaviPro
const API_BASE = 'https://your-repl.username.repl.co';

// Pencarian lokasi
async function searchLocation(query) {
    const response = await fetch(`${API_BASE}/api/search?q=${query}`);
    return await response.json();
}

// Data region
async function getRegionData(city) {
    const response = await fetch(`${API_BASE}/api/locations/${city}`);
    return await response.json();
}
```

## 🛠️ Development

### Menambah Data Baru
1. Tambahkan file JSON ke `main/raw-data/`
2. Push ke repository
3. GitHub Actions akan memproses otomatis

### Format Data Input
Data JSON harus mengikuti format:
```json
[
    {
        "title": "Nama Lokasi",
        "place_id": "unique_id",
        "address": "Alamat lengkap",
        "city": "Nama Kota",
        "gps_coordinates": {
            "latitude": -8.123,
            "longitude": 115.456
        },
        "phone": "+62...",
        "website": "https://..."
    }
]
```

## 📈 Monitoring

- **Web Interface**: Akses `/` untuk dashboard
- **Health Check**: Endpoint `/health` untuk monitoring
- **Logs**: Console output untuk debugging

## 🤝 Kontribusi

1. Fork repository
2. Buat branch fitur: `git checkout -b feature/nama-fitur`
3. Commit perubahan: `git commit -m 'Tambah fitur'`
4. Push ke branch: `git push origin feature/nama-fitur`
5. Buat Pull Request

## 📝 Lisensi

Repository ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

## 🔗 Links

- **GitHub**: https://github.com/tjx578/datalokasi_maps
- **Issues**: https://github.com/tjx578/datalokasi_maps/issues
- **Wiki**: https://github.com/tjx578/datalokasi_maps/wiki
