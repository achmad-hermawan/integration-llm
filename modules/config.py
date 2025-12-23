# modules/config.py

# Nama File Database
DB_NAME = 'sales_data.db'

# Nama Model Ollama (Pastikan sudah di-download via terminal)
MODEL_NAME = 'llama3.1' 

# Judul Aplikasi
APP_TITLE = "🛡️ Nexus Enterprise: Secure SQL Ops"

# System Prompt (Otak Analis)
# Senior Dev Tip: Prompt ditaruh sini biar mudah diedit tanpa ngacak-ngacak logic.
SYSTEM_PROMPT = """
You are a strict SQL Expert using SQLite.
Schema:
1. products(id, name, price, stock)
2. customers(id, name, email, city)
3. sales(id, customer_id, product_id, quantity, date)

RULES:
1. Output ONLY the raw SQL query. No markdown, no comments.
2. Only use SELECT statements. 
3. If the user asks something not related to data, respond with: SELECT 'Maaf, diluar konteks data'
"""