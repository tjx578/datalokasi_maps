# Data Lokasi Maps - Location Data Processing Pipeline

This repository is an automated location data processing pipeline that consolidates, deduplicates, and structures location data (primarily Indonesian health facilities) from raw JSON files into organized outputs.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Environment Setup
- **Python Required**: Python 3.12+ (test with `python3 --version`)
- **No Dependencies**: Uses only Python standard library (json, csv, os, collections)
- **No requirements.txt**: The repository uses no external dependencies
- **jq Required**: JSON validation uses `jq` (pre-installed on Ubuntu runners)

### Core Workflow Commands
Run these commands in sequence to process data:

```bash
# 1. Process raw data (NEVER CANCEL: completes in <2 seconds)
time python3 process.py

# 2. Validate all JSON outputs (NEVER CANCEL: completes in <3 seconds)
time bash -c "shopt -s globstar nullglob; for f in **/*.json; do echo \"checking \$f\"; jq -e . \"\$f\" >/dev/null; done"
```

**CRITICAL TIMING**: 
- Data processing: <1 second. Set timeout to 30+ seconds.
- JSON validation: ~2 seconds for 150+ files. Set timeout to 30+ seconds.
- NEVER CANCEL these operations - they complete very quickly.

### Repository Structure
```
.
├── raw-data/              # Input: Raw JSON files (56 files, ~24MB)
│   ├── .gitkeep
│   └── *.json            # Location data files
├── process.py            # Main processing script
├── output-json/          # Generated: Split JSON files by city/region  
│   └── *.json           # ~100+ regional files
├── output-data.csv       # Generated: Summary CSV (name, place_id, city)
├── .github/
│   └── wrokflows/       # Note: typo in folder name "wrokflows"
│       └── process.yml  # GitHub Actions automation
├── README.md
└── WORKFLOW_INSTRUKSI.md # Workflow documentation in Indonesian
```

## Data Processing Details

### Input Format
- **Source**: JSON files in `raw-data/` containing location records
- **Record Count**: ~10,332 raw records → ~5,042 after deduplication
- **Data Fields**: place_id, title/name, city, state, coordinates, ratings, etc.
- **Content**: Primarily Indonesian health facilities (Puskesmas, clinics, hospitals)

### Processing Logic (`process.py`)
1. **Combine**: Loads all JSON files from `raw-data/`
2. **Deduplicate**: Removes duplicates based on `place_id` 
3. **Group**: Organizes records by city/state field
4. **Output**: Creates separate JSON files per region + summary CSV

### Expected Outputs
- **Regional JSON files**: ~100+ files in `output-json/` (e.g., `gianyar_regency.json`)
- **Summary CSV**: `output-data.csv` with columns: name, place_id, city
- **Processing time**: <1 second for 24MB of input data
- **File counts**: 56 input files → 100+ output files + 1 CSV

## Validation and Testing

### Manual Validation Workflow
Always run this complete validation after making changes:

```bash
# 1. Clean previous outputs
rm -rf output-json output-data.csv

# 2. Run processing and time it
time python3 process.py

# 3. Verify outputs were created
ls -la output-json/ | wc -l  # Should show ~100+ files
wc -l output-data.csv        # Should show ~5000+ lines

# 4. Validate JSON syntax for ALL files
time bash -c "shopt -s globstar nullglob; for f in **/*.json; do jq -e . \"\$f\" >/dev/null || echo \"FAILED: \$f\"; done"

# 5. Test sample data structure
jq '.[0] | keys' output-json/gianyar_regency.json  # Should show 60+ field names
```

**Expected Results**:
- Processing: "Total records mentah: 10332", "Setelah dedup: 5042"
- Output: 100+ regional JSON files + 1 CSV file
- Validation: All JSON files pass `jq` syntax check
- Timing: Total validation workflow completes in <5 seconds

### Data Quality Checks
- **Deduplication**: Verify `place_id` uniqueness within each regional file
- **Completeness**: Check that total CSV rows ≈ total deduplicated records
- **Regional Distribution**: Largest regions (Gianyar: ~1300, Denpasar: ~1200, Badung: ~700)

## GitHub Actions Automation

### Workflow Trigger
- **File**: `.github/wrokflows/process.yml` (note: folder has typo)
- **Triggers**: 
  - Push to `main` branch with changes to `main/raw-data/**` or `main/process.py`
  - Manual dispatch via `workflow_dispatch`
- **Note**: Workflow paths reference `main/` prefix but repository structure is flat

### Workflow Issues
- **Path Mismatch**: Workflow expects `main/raw-data/` but actual path is `raw-data/`
- **Folder Typo**: `.github/wrokflows/` should be `.github/workflows/`
- **Branch Reference**: Workflow triggers on `main` branch changes

## Common Tasks

### Adding New Raw Data
1. Place JSON files in `raw-data/` directory
2. Run `python3 process.py` to regenerate outputs
3. Validate with JSON syntax check
4. Commit both raw data and generated outputs

### Debugging Processing Issues
- **Memory Issues**: Processing 24MB should complete in <1 second
- **JSON Errors**: Use `jq -e . "filename.json"` to validate specific files
- **Empty Outputs**: Check that input files contain valid JSON arrays
- **Missing Cities**: Verify `city` or `state` fields exist in source data

### File Structure Verification
```bash
# Check repository structure
ls -la  # Should show: .github/, raw-data/, process.py, README.md, WORKFLOW_INSTRUKSI.md

# Count input files and size
find raw-data -name "*.json" | wc -l  # Should show 56
du -h raw-data/                       # Should show ~24MB

# Check for outputs after processing
ls output-json/ | wc -l              # Should show 100+
head -5 output-data.csv              # Should show: name,place_id,city header + data
```

## Key Repository Information

### Current State
- **Input Files**: 56 JSON files (~24MB) in `raw-data/`
- **Processing Speed**: Sub-second processing time
- **Output Scale**: 100+ regional files + summary CSV
- **Data Focus**: Indonesian location data, primarily health facilities
- **Automation**: GitHub Actions workflow (with path issues noted above)

### Data Pipeline Summary
Raw JSON → Python Processing → Regional JSON + CSV → Validation → Git Commit

**Always run the complete validation workflow after any changes to ensure data integrity and processing correctness.**