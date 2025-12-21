import sqlite3
import pandas as pd

def run_query(query):
    """
    Menjalankan query SQL pada database SQLite sales_data.db
    Mengembalikan: DataFrame (jika sukses), Error Message (jika gagal)
    """
    try:
        conn = sqlite3.connect('sales_data.db')
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)