import streamlit as st
import pandas as pd
import os

# Inisialisasi Database sederhana
DB_FILE = "sun_ledger_data.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["ID", "Tanggal", "Tipe", "Kategori", "Nominal", "Catatan"])
    df.to_csv(DB_FILE, index=False)

st.set_page_config(page_title="Sun Ledger", page_icon="☀️", layout="wide")

# Sidebar Navigation - Diganti ke Selectbox agar mudah ditekan di HP
st.sidebar.title("☀️ Sun Ledger")
menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Sun Statement", "Sun Wealth", "Sun Equity & Recovery"])

if menu == "Home":
    st.title("Selamat Datang di Sun Ledger ☀️")
    st.write("Aplikasi pencatatan cash flow personal bisnis Anda.")
    st.markdown("""
    - **Sun Statement:** Pencatatan transaksi harian (Cash In & Out).
    - **Sun Wealth:** Laporan visual bulanan dan revenue.
    - **Sun Equity & Recovery:** Tracking balik modal & kerugian investasi.
    """)
    
elif menu == "Sun Statement":
    import sun_statement
    sun_statement.run()
    
elif menu == "Sun Wealth":
    import sun_wealth
    sun_wealth.run()
    
elif menu == "Sun Equity & Recovery":
    import sun_equity
    sun_equity.run()