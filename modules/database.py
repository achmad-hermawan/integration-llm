# modules/database.py
import sqlite3
import pandas as pd
import logging
from .config import DB_NAME

# Setup Logging (Biar kelihatan profesional di terminal)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DatabaseGuard")

def is_query_safe(query):
    """
    🛡️ SECURITY LAYER:
    Mencegah perintah berbahaya (DELETE, DROP, UPDATE).
    """
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
    query_upper = query.upper()
    
    for word in dangerous_keywords:
        if word in query_upper:
            logger.warning(f"⛔ BLOCKED Dangerous Query: {query}")
            return False, f"SECURITY ALERT: Perintah '{word}' diblokir demi keamanan sistem."
    
    return True, ""

def run_query(query):
    """
    Menjalankan query SQL dengan aman.
    """
    # 1. Cek Keamanan
    is_safe, message = is_query_safe(query)
    if not is_safe:
        return None, message

    # 2. Eksekusi Query
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return None, "Query berhasil, tapi data kosong (0 rows)."
            
        return df, None

    except Exception as e:
        logger.error(f"SQL Execution Error: {e}")
        return None, f"Database Error: {str(e)}"