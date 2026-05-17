# ETL Employee Data Pipeline

> Automated data pipeline that extracts raw CSV data, cleans it, loads it into MySQL, and generates a formatted Excel report — built with Python, Pandas, and MySQL.

---

## What This Pipeline Does

| Stage | Description |
|---|---|
| **Extract** | Reads raw employee CSV data (210 rows with intentional dirty data) |
| **Transform** | Removes duplicates, fixes date formats, handles missing values, cleans salary data |
| **Load** | Inserts clean data into MySQL with upsert logic |
| **Report** | Generates styled Excel report with 3 sheets |

---

## Results

- **210 rows** raw input → **188 rows** clean output
- **10 duplicate rows** removed automatically
- **12 rows** with missing critical fields dropped
- Missing salaries filled with **median value (Rp 11,350,885)**
- Date formats standardized from mixed formats (`DD/MM/YYYY`, `MM-DD-YYYY`) to `YYYY-MM-DD`

---

## Tech Stack

- **Python 3.14** — core pipeline logic
- **Pandas** — data cleaning and transformation
- **MySQL 8.0** — data storage
- **mysql-connector-python** — database connection
- **openpyxl** — Excel report generation
- **Faker** — realistic dummy data generation

---

## Project Structure

```
├── generate_data.py     # Generate realistic dirty CSV data (200+ rows)
├── etl_pipeline.py      # Main ETL: Extract → Transform → Load to MySQL
├── report.py            # Generate styled Excel report from MySQL
├── requirements.txt     # Python dependencies
└── .gitignore
```

---

## Excel Report Output

The report generates 3 sheets automatically:

- **All Employees** — complete clean dataset
- **Department Summary** — headcount, avg/min/max salary per department
- **Status Summary** — Active vs Inactive breakdown with avg salary

---

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL 8.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/MuzakkiAley/etl-employee-pipeline.git
cd etl-employee-pipeline

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Open `etl_pipeline.py` and `report.py`, update the DB config:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Muzzasql03#',
    'database': 'employee_db'
}
```

### Run

```bash
# Step 1: Generate raw CSV data
python generate_data.py

# Step 2: Run ETL pipeline
python etl_pipeline.py

# Step 3: Generate Excel report
python report.py
```

---

## Sample Pipeline Output

```
==================================================
  ETL PIPELINE — Employee Data
==================================================
[EXTRACT] Reading employees_raw.csv...
  Loaded 210 rows, 8 columns

[TRANSFORM] Cleaning data...
  Removed 10 duplicate rows
  Removed 12 rows with missing name/email/department
  Salary cleaned (median fill: Rp 11,350,885)
  Dates standardized to YYYY-MM-DD
  Final clean rows: 188 (from 210)

[LOAD] Connecting to MySQL...
  Inserted/updated 125 rows, skipped 63

[DONE] Pipeline completed successfully!
```

---

## Author

**Ahmad Muzakki Aley**
Teknik Informatika — STMIK IKMI Cirebon, 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/ahmadmuzakkialey)
[![Email](https://img.shields.io/badge/Email-ahmadmuzakkialey@gmail.com-red)](mailto:ahmadmuzakkialey@gmail.com)

---

## Certifications

- Data Engineering Master Certification — RapidMiner (Altair)
- Data Engineering Professional Certification — RapidMiner (Altair)
- Programming Essentials in Python — Cisco / OpenEDG Python Institute

Keywords: `Python` `ETL` `Data Pipeline` `MySQL` `Pandas` `Data Engineering` `Excel Automation`
