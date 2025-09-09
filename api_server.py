#!/usr/bin/env python3
"""
API Server untuk NaviPro - Penyedia Database Lokasi Maps
Melayani data lokasi yang telah diproses untuk kebutuhan navigasi NaviPro
"""

import os
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Konfigurasi path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON_DIR = os.path.join(BASE_DIR, "main", "output-json")
OUTPUT_CSV_FILE = os.path.join(BASE_DIR, "main", "output-data.csv")

@app.route('/')
def home():
    """Web interface untuk NaviPro Location Database"""
    return render_template('index.html')

@app.route('/api')
def api_info():
    """Endpoint informasi API"""
    return jsonify({
        "name": "NaviPro Location Database API",
        "version": "1.0.0",
        "description": "Penyedia database lokasi maps untuk NaviPro",
        "endpoints": {
            "/": "Web interface",
            "/api": "Informasi API",
            "/health": "Status kesehatan server",
            "/api/locations": "Daftar semua lokasi",
            "/api/locations/<city>": "Lokasi berdasarkan kota/kabupaten",
            "/api/search?q=<query>": "Pencarian lokasi",
            "/api/regions": "Daftar semua region yang tersedia",
            "/api/stats": "Statistik database"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Server NaviPro Location Database berjalan normal"})

@app.route('/api/regions')
def get_regions():
    """Mendapatkan daftar semua region yang tersedia"""
    try:
        if not os.path.exists(OUTPUT_JSON_DIR):
            return jsonify({"error": "Data belum diproses"}), 404
            
        regions = []
        for filename in os.listdir(OUTPUT_JSON_DIR):
            if filename.endswith('.json'):
                region_name = filename.replace('.json', '').replace('_', ' ').title()
                file_path = os.path.join(OUTPUT_JSON_DIR, filename)
                
                # Hitung jumlah lokasi di region ini
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        location_count = len(data) if isinstance(data, list) else 0
                except:
                    location_count = 0
                
                regions.append({
                    "id": filename.replace('.json', ''),
                    "name": region_name,
                    "location_count": location_count
                })
        
        regions.sort(key=lambda x: x['location_count'], reverse=True)
        
        return jsonify({
            "total_regions": len(regions),
            "regions": regions
        })
        
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data region: {str(e)}"}), 500

@app.route('/api/locations')
def get_all_locations():
    """Mendapatkan semua lokasi (dengan pagination)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        if not os.path.exists(OUTPUT_CSV_FILE):
            return jsonify({"error": "Data CSV belum tersedia"}), 404
        
        locations = []
        with open(OUTPUT_CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                locations.append(row)
        
        total = len(locations)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_locations = locations[start:end]
        
        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "locations": paginated_locations
        })
        
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data lokasi: {str(e)}"}), 500

@app.route('/api/locations/<city>')
def get_locations_by_city(city):
    """Mendapatkan lokasi berdasarkan kota/kabupaten"""
    try:
        city_file = city.replace(' ', '_').lower()
        file_path = os.path.join(OUTPUT_JSON_DIR, f"{city_file}.json")
        
        if not os.path.exists(file_path):
            return jsonify({"error": f"Data untuk {city} tidak ditemukan"}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            "city": city,
            "total_locations": len(data),
            "locations": data
        })
        
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data untuk {city}: {str(e)}"}), 500

@app.route('/api/search')
def search_locations():
    """Pencarian lokasi berdasarkan nama"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({"error": "Parameter 'q' diperlukan untuk pencarian"}), 400
        
        results = []
        
        # Cari di semua file JSON
        if os.path.exists(OUTPUT_JSON_DIR):
            for filename in os.listdir(OUTPUT_JSON_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(OUTPUT_JSON_DIR, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        for location in data:
                            name = location.get('title', location.get('name', '')).lower()
                            if query in name:
                                location['region'] = filename.replace('.json', '')
                                results.append(location)
                    except:
                        continue
        
        return jsonify({
            "query": query,
            "total_results": len(results),
            "results": results[:100]  # Batasi hasil maksimal 100
        })
        
    except Exception as e:
        return jsonify({"error": f"Gagal melakukan pencarian: {str(e)}"}), 500

@app.route('/api/stats')
def get_stats():
    """Statistik database"""
    try:
        stats = {
            "total_regions": 0,
            "total_locations": 0,
            "top_regions": []
        }
        
        if os.path.exists(OUTPUT_JSON_DIR):
            region_stats = []
            for filename in os.listdir(OUTPUT_JSON_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(OUTPUT_JSON_DIR, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            count = len(data) if isinstance(data, list) else 0
                            region_stats.append({
                                "region": filename.replace('.json', ''),
                                "count": count
                            })
                            stats["total_locations"] += count
                    except:
                        continue
            
            stats["total_regions"] = len(region_stats)
            region_stats.sort(key=lambda x: x['count'], reverse=True)
            stats["top_regions"] = region_stats[:10]
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil statistik: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)