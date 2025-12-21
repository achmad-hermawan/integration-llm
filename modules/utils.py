import streamlit as st
import pandas as pd

def load_css(file_name):
    """Membaca file CSS dan menyuntikkannya ke Streamlit"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_demo_response(user_prompt):
    """
    Menghasilkan data palsu (Mock Data) saat API Limit habis
    """
    prompt_lower = user_prompt.lower()
    
    if "produk" in prompt_lower:
        sql = "SELECT name, price, stock FROM products ORDER BY price DESC LIMIT 5"
        df = pd.DataFrame({
            "name": ["Laptop Gaming X", "Monitor 4K Sony", "Headset Pro", "Keyboard Mech", "Mouse Wireless"],
            "price": [15000000, 5000000, 2000000, 1500000, 500000],
            "stock": [10, 25, 50, 30, 100]
        })
    elif "pelanggan" in prompt_lower:
        sql = "SELECT * FROM customers WHERE city = 'Jakarta'"
        df = pd.DataFrame({
            "name": ["Budi Santoso", "Citra Kirana", "Dewi Sartika"],
            "city": ["Jakarta", "Jakarta", "Jakarta"],
            "email": ["budi@gmail.com", "citra@ymail.com", "dewi@outlook.com"]
        })
    else:
        sql = "SELECT count(*) as total_sales FROM sales"
        df = pd.DataFrame({"total_sales": [154], "revenue": ["Rp 250.000.000"]})
        
    return sql, df