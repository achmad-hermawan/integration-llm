import google.generativeai as genai

SYSTEM_PROMPT = """
Kamu adalah AI Data Analyst. Tugasmu mengubah pertanyaan user menjadi Query SQL SQLite.
Skema: products(id, name, price, stock), customers(id, name, email, city), sales(id, customer_id, product_id, quantity, date).
Aturan: Hanya output SQL. Tanpa markdown. Tanpa penjelasan.
"""

def get_sql_from_ai(user_question, api_key):
    """
    Mengirim prompt ke Google Gemini dan mendapatkan balasan SQL murni.
    """
    if not api_key:
        return "ERROR: API Key Kosong"

    genai.configure(api_key=api_key)
    # Gunakan model hemat
    model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=SYSTEM_PROMPT)
    
    try:
        response = model.generate_content(user_question)
        # Bersihkan string dari backticks markdown
        clean_sql = response.text.replace("```sql", "").replace("```", "").strip()
        return clean_sql
    except Exception as e:
        return f"ERROR: {str(e)}"