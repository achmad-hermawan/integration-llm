import streamlit as st
from modules.config import APP_TITLE
from modules.llm import get_sql_from_llama
from modules.database import run_query
from modules.utils import load_css # Pastikan file utils.py ada (lihat step sebelumnya)

# 1. Setup Halaman
st.set_page_config(page_title="Nexus Secure", page_icon="🛡️", layout="wide")

# 2. Load CSS (Opsional, kalau file assets/style.css ada)
try:
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except:
    pass

# 3. Sidebar
with st.sidebar:
    st.title("🛡️ Secure Ops")
    st.info("System: **ONLINE**")
    st.markdown("---")
    st.write("**Model:** LLaMA 3.1 (Local)")
    st.write("**Mode:** Read-Only Access")
    
    if st.button("Clear Log"):
        st.session_state.messages = []
        st.rerun()

# 4. Header
st.title(APP_TITLE)
st.caption("Architecture: Modular Python + Local LLM + SQL Sanitization Layer")

# 5. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Security System Active. Silakan request data penjualan."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "dataframe":
            st.dataframe(msg["content"])
        elif msg.get("type") == "error":
            st.error(msg["content"])
        else:
            st.markdown(msg["content"])

# 6. Logic Utama
if prompt := st.chat_input("Masukkan perintah query..."):
    # Tampilkan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔒 Verifying protocol & Generating SQL..."):
            
            # STEP A: Generate SQL (AI Layer)
            sql_query = get_sql_from_llama(prompt)
            
            if "ERROR" in sql_query:
                st.error(sql_query)
            else:
                # Tampilkan Code SQL (Transparansi)
                st.code(sql_query, language="sql")
                st.session_state.messages.append({"role": "assistant", "content": f"```sql\n{sql_query}\n```"})
                
                # STEP B: Execute SQL (Database Layer with Security)
                df_result, err_msg = run_query(sql_query)
                
                if err_msg:
                    # Jika kena blokir security atau error DB
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg, "type": "error"})
                elif df_result is not None:
                    # Jika sukses
                    st.success(f"Data Retrieved: {len(df_result)} records.")
                    st.dataframe(df_result)
                    st.session_state.messages.append({"role": "assistant", "content": df_result, "type": "dataframe"})