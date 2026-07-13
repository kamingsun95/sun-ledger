import streamlit as st
import pandas as pd
from datetime import datetime
import os

DB_FILE = "sun_ledger_data.csv"

# Harga default paket
DEFAULT_PRICES = {
    "Plus": 150000,
    "Premium": 300000,
    "VIP": 500000,
    "Comic": 100000,
    "Kostum": 0  # Kostum biasanya custom
}

def run():
    st.title("📝 Sun Statement")
    st.write("Catat pemasukan dan pengeluaran harianmu di sini.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cash In (Uang Masuk)")
        with st.form("cash_in_form"):
            paket = st.selectbox("Pilih Paket", list(DEFAULT_PRICES.keys()))
            nominal = st.number_input("Nominal (Rp)", min_value=0, value=DEFAULT_PRICES[paket], step=10000)
            catatan = st.text_input("Catatan (Opsional)")
            submit_in = st.form_submit_button("Submit Cash In")
            
            if submit_in:
                new_data = pd.DataFrame([{
                    "Tanggal": datetime.now(),
                    "Tipe": "Cash In",
                    "Kategori": paket,
                    "Nominal": nominal,
                    "Catatan": catatan
                }])
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Berhasil mencatat Cash In: {paket} sebesar Rp {nominal:,.0f}".replace(",", "."))
                st.rerun()

    with col2:
        st.subheader("Cash Out (Uang Keluar)")
        with st.form("cash_out_form"):
            kategori_out = st.selectbox("Pilih Kategori", ["KAS", "Expense", "Spending"])
            nominal_out = st.number_input("Nominal Pengeluaran (Rp)", min_value=0, value=0, step=10000)
            catatan_out = st.text_input("Catatan Pengeluaran (Opsional)")
            submit_out = st.form_submit_button("Submit Cash Out")
            
            if submit_out:
                new_data = pd.DataFrame([{
                    "Tanggal": datetime.now(),
                    "Tipe": "Cash Out",
                    "Kategori": kategori_out,
                    "Nominal": nominal_out,
                    "Catatan": catatan_out
                }])
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Berhasil mencatat Cash Out: {kategori_out} sebesar Rp {nominal_out:,.0f}".replace(",", "."))
                st.rerun()

    # Fitur History & Hapus Hari Ini
    st.divider()
    st.subheader("Riwayat Transaksi Hari Ini")
    df = pd.read_csv(DB_FILE)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    today = datetime.now().date()
    df_today = df[df['Tanggal'].dt.date == today]
    
    if not df_today.empty:
        st.dataframe(df_today[['Tanggal', 'Tipe', 'Kategori', 'Nominal', 'Catatan']], use_container_width=True)
        if st.button("Hapus Transaksi Terakhir"):
            df = df[:-1]  # Hapus baris terakhir
            df.to_csv(DB_FILE, index=False)
            st.rerun()
    else:
        st.info("Belum ada transaksi hari ini.")