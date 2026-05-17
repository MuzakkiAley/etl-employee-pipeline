import pandas as pd
import mysql.connector
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Muzzasql03#',  # ganti dengan password MySQL kamu
    'database': 'employee_db'
}

CSV_FILE = 'employees_raw.csv'

# ─── EXTRACT ──────────────────────────────────────────────
def extract(filepath):
    print(f"\n[EXTRACT] Reading {filepath}...")
    df = pd.read_csv(filepath)
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    return df

# ─── TRANSFORM ────────────────────────────────────────────
def transform(df):
    print(f"\n[TRANSFORM] Cleaning data...")
    original_count = len(df)

    # 1. Remove duplicates
    df = df.drop_duplicates(subset='employee_id')
    print(f"  Removed {original_count - len(df)} duplicate rows")

    # 2. Drop rows with missing critical fields
    before = len(df)
    df = df.dropna(subset=['name', 'email', 'department'])
    print(f"  Removed {before - len(df)} rows with missing name/email/department")

    # 3. Clean salary: remove non-numeric, fill missing with median
    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
    median_salary = df['salary'].median()
    df['salary'] = df['salary'].fillna(median_salary).astype(int)
    print(f"  Salary cleaned (median fill: Rp {median_salary:,.0f})")

    # 4. Standardize date format to YYYY-MM-DD
    def parse_date(val):
        if pd.isna(val):
            return None
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y'):
            try:
                return datetime.strptime(str(val), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None

    df['join_date'] = df['join_date'].apply(parse_date)
    print(f"  Dates standardized to YYYY-MM-DD")

    # 5. Standardize status column
    df['status'] = df['status'].str.strip().str.title()

    print(f"\n  Final clean rows: {len(df)} (from {original_count})")
    return df

# ─── LOAD ─────────────────────────────────────────────────
def load(df):
    print(f"\n[LOAD] Connecting to MySQL...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create database and table
    cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
    cursor.execute("USE employee_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            department VARCHAR(50),
            salary INT,
            join_date DATE,
            status VARCHAR(20),
            phone VARCHAR(30),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert rows
    inserted = 0
    skipped = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO employees 
                    (employee_id, name, email, department, salary, join_date, status, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    salary = VALUES(salary),
                    status = VALUES(status)
            """, (
                row['employee_id'], row['name'], row['email'],
                row['department'], int(row['salary']),
                row['join_date'], row['status'], row['phone']
            ))
            inserted += 1
        except Exception as e:
            skipped += 1

    conn.commit()
    print(f"  Inserted/updated {inserted} rows, skipped {skipped}")
    cursor.close()
    conn.close()
    return inserted

# ─── MAIN ─────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  ETL PIPELINE — Employee Data")
    print("=" * 50)

    raw_df = extract(CSV_FILE)
    clean_df = transform(raw_df)
    load(clean_df)

    print(f"\n[DONE] Pipeline completed successfully!")
    print("  Run report.py to generate Excel report.")