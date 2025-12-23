# modules/llm.py
import ollama
import re
from .config import MODEL_NAME, SYSTEM_PROMPT

def get_sql_from_llama(user_input):
    """
    Mengirim prompt ke LLaMA lokal dan membersihkan outputnya.
    """
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_input}
        ])
        
        raw_content = response['message']['content']
        
        # CLEANING: Hapus backticks markdown (```sql ... ```)
        clean_sql = re.sub(r"```sql|```", "", raw_content, flags=re.IGNORECASE).strip()
        
        # EXTRA CLEANING: Ambil hanya bagian SELECT pertama (jika AI "cerewet")
        match = re.search(r"(SELECT.*)", clean_sql, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
        
        return clean_sql

    except Exception as e:
        return f"ERROR: Gagal koneksi ke Ollama. ({str(e)})"