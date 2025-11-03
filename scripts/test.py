# scripts/run_queries.py
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

def test_connection():
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print("✅ Connection successful!")
        print("PostgreSQL version:", version[0])
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()
