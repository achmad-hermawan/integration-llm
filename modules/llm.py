import google.generativeai as genai

SYSTEM_PROMPT = """
Kamu adalah AI Data Analyst. Tugasmu mengubah pertanyaan user menjadi Query SQL SQLite.
Skema:
- products(id, name, price, stock)
- customers(id, name, email, city)
- sales(id, customer_id, product_id, quantity, date)

Aturan:
- Hanya output SQL
- Tanpa markdown
- Tanpa penjelasan
"""

def get_sql_from_ai(user_question, api_key):
    if not api_key:
        return "ERROR: API Key kosong"

    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-pro-latest",
            system_instruction=SYSTEM_PROMPT
        )

        response = model.generate_content(user_question)

        if not response.text:
            return "ERROR: Response kosong dari model"

        return (
            response.text
            .replace("```sql", "")
            .replace("```", "")
            .strip()
        )

    except Exception as e:
        return f"ERROR: {e}"
