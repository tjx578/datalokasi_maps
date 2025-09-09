# Quick Start Guide: NaviPro Location Database

## 🚀 Deploy to Replit (Recommended for NaviPro)

1. **Import Repository**
   - Go to [Replit](https://replit.com/)
   - Click "Create Repl" → "Import from GitHub"
   - Enter: `https://github.com/tjx578/datalokasi_maps`

2. **Auto Setup**
   - Replit will automatically detect Python and install dependencies
   - The `.replit` file configures everything automatically

3. **Run the Server**
   - Click the "Run" button in Replit
   - The API server will start at your Replit URL

4. **Access Your API**
   - Your API will be available at: `https://your-repl-name.username.repl.co`
   - Web interface: `https://your-repl-name.username.repl.co/`
   - API endpoints: `https://your-repl-name.username.repl.co/api/...`

## 📡 API Integration for NaviPro

### Base URL
```javascript
const API_BASE = 'https://your-repl-name.username.repl.co';
```

### Common NaviPro Use Cases

#### 1. Search Locations
```javascript
async function searchLocations(query) {
    const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.results; // Array of locations
}

// Usage
const schools = await searchLocations('sekolah');
const restaurants = await searchLocations('restoran');
```

#### 2. Get Region Data
```javascript
async function getRegionData(cityName) {
    const response = await fetch(`${API_BASE}/api/locations/${cityName}`);
    const data = await response.json();
    return data.locations; // Array of locations in the city
}

// Usage
const denpasar = await getRegionData('denpasar_city');
const gianyar = await getRegionData('gianyar_regency');
```

#### 3. Get Available Regions
```javascript
async function getAvailableRegions() {
    const response = await fetch(`${API_BASE}/api/regions`);
    const data = await response.json();
    return data.regions; // Array of {id, name, location_count}
}
```

#### 4. Database Statistics
```javascript
async function getDatabaseStats() {
    const response = await fetch(`${API_BASE}/api/stats`);
    return await response.json();
}
```

### Response Format

#### Location Object
```json
{
    "title": "SD Negeri 27 Pemecutan",
    "place_id": "ChIJQwykxLZA0i0RdtLdDlvpddI",
    "address": "Jl. Gn. Cemara Raya No.23, Tegal Harum...",
    "city": "Denpasar City",
    "state": "Bali",
    "gps_coordinates": {
        "latitude": -8.667012999999999,
        "longitude": 115.196975
    },
    "phone": "+62 361 486769",
    "website": "https://sdn27-pemecutan.sch.id/",
    "type": "Elementary school"
}
```

## 🔧 Local Development

If you prefer to run locally:

```bash
# Clone repository
git clone https://github.com/tjx578/datalokasi_maps.git
cd datalokasi_maps

# Install dependencies
pip install -r requirements.txt

# Process data (if needed)
cd main && python process.py && cd ..

# Start API server
python api_server.py
```

## 📊 Available Data

- **Total Locations**: 6,918 locations
- **Regions**: 200+ cities/regencies
- **Categories**: Schools, businesses, religious sites, public facilities
- **Coverage**: Primarily Bali, with additional Indonesia and international locations

### Top Regions by Location Count:
1. Gianyar Regency: 1,307 locations
2. Denpasar City: 1,213 locations  
3. Jembrana Regency: 825 locations
4. Tabanan Regency: 814 locations
5. Badung Regency: 740 locations

## 🏥 Health Monitoring

Check if your API is healthy:
```javascript
const health = await fetch(`${API_BASE}/health`);
const status = await health.json();
console.log(status.message); // "Server NaviPro Location Database berjalan normal"
```

## 📝 Rate Limiting & Best Practices

- No rate limiting currently implemented
- Pagination available for large datasets (`?page=1&per_page=50`)
- Use specific region endpoints for better performance
- Cache results when possible in your NaviPro application

## 🆘 Troubleshooting

### Common Issues:

1. **Repl not starting**: Check if all files are properly uploaded
2. **Empty results**: Verify the region name format (use underscores, lowercase)
3. **Slow queries**: Use specific region endpoints instead of searching all data

### Debug Endpoints:
- `/health` - Check server status
- `/api/stats` - Database statistics
- `/api/regions` - List all available regions

## 📞 Support

For issues specific to this location database:
- GitHub Issues: https://github.com/tjx578/datalokasi_maps/issues
- Check the main README.md for detailed documentation