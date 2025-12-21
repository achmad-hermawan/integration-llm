import streamlit as st
import time

# --- IMPORT MODULE BUATAN SENDIRI ---
from modules.database import run_query
from modules.llm import get_sql_from_ai
from modules.utils import load_css, get_demo_response

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Nexus Data Assistant",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. LOAD DESAIN DARI FILE TERPISAH
load_css("assets/style.css")

# 3. SIDEBAR & NAVIGASI
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("### ⚙️ Control Panel")
    
    api_key = st.text_input("🔑 Google API Key", type="password")
    st.markdown("---")
    
    st.markdown("### 🛠️ Developer Mode")
    demo_mode = st.toggle("Nyala Mode Demo (Fake AI)", value=False, 
                          help="Gunakan ini jika API Error untuk keperluan Screenshot.")
    
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# 4. HEADER UTAMA
st.title("🔮 NEXUS: Enterprise SQL Assistant")

# Metrik Dashboard (Pemanis UI)
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", "1,240", "Live")
col2.metric("API Latency", "45ms", "-12ms")
col3.metric("System Status", "Optimal", delta_color="normal")
st.markdown("---")

# 5. LOGIKA CHAT
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Halo! Nexus Analytics siap. Silakan tanya data penjualan."}
    ]

# Render History Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        if msg.get("type") == "dataframe":
            st.dataframe(msg["content"], use_container_width=True)
        else:
            st.markdown(msg["content"])

# 6. INPUT USER & PROSES
if prompt := st.chat_input("Contoh: Tampilkan pelanggan dari Jakarta"):
    
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respon Bot
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        # --- JALUR 1: MODE DEMO (UNTUK SCREENSHOT AMAN) ---
        if demo_mode:
            with st.spinner("🔄 Simulasi Mode Demo..."):
                time.sleep(1.5)
                fake_sql, fake_df = get_demo_response(prompt)
                
                message_placeholder.markdown(f"**Generated SQL (Demo):**\n```sql\n{fake_sql}\n```")
                st.dataframe(fake_df, use_container_width=True)
                
                st.session_state.messages.append({"role": "assistant", "content": f"**Generated SQL:**\n```sql\n{fake_sql}\n```"})
                st.session_state.messages.append({"role": "assistant", "content": fake_df, "type": "dataframe"})

        # --- JALUR 2: MODE ASLI (AI + DB NYATA) ---
        else:
            if not api_key:
                st.error("⚠️ API Key belum dimasukkan!")
                st.stop()
                
            with st.spinner("📡 Menghubungi AI..."):
                generated_sql = get_sql_from_ai(prompt, api_key)
                
                if "ERROR" in generated_sql:
                    st.error("🚦 Limit API Google Habis. Silakan nyalakan **Mode Demo** di sidebar.")
                elif "SELECT" not in generated_sql.upper():
                    st.markdown(generated_sql)
                    st.session_state.messages.append({"role": "assistant", "content": generated_sql})
                else:
                    # Tampilkan SQL
                    message_placeholder.markdown(f"```sql\n{generated_sql}\n```")
                    st.session_state.messages.append({"role": "assistant", "content": f"```sql\n{generated_sql}\n```"})
                    
                    # Jalankan SQL ke Database
                    df_result, err = run_query(generated_sql)
                    
                    if err:
                        st.error(f"SQL Error: {err}")
                    else:
                        st.dataframe(df_result, use_container_width=True)
                        st.session_state.messages.append({"role": "assistant", "content": df_result, "type": "dataframe"})