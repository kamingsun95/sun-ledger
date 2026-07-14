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
    "Kostum": 0
}

def format_rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

def run():
    st.title("📝 Sun Statement")
    st.write("Catat pemasukan dan pengeluaran harianmu di sini.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cash In (Uang Masuk)")
        with st.form("cash_in_form"):
            paket = st.selectbox("Pilih Paket", list(DEFAULT_PRICES.keys()))
            nominal = st.number_input("Nominal (Rp)", min_value=0, value=DEFAULT_PRICES[paket], step=10000, format="%d")
            catatan = st.text_input("Catatan (Opsional)")
            submit_in = st.form_submit_button("Submit Cash In")
            
            if submit_in:
                new_data = pd.DataFrame([{
                    "Tanggal": datetime.now(),
                    "Tipe": "Cash In",
                    "Kategori": paket,
                    "Nominal": int(nominal),
                    "Catatan": catatan
                }])
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Berhasil mencatat Cash In: {paket} sebesar {format_rupiah(nominal)}")
                st.rerun()

    with col2:
        st.subheader("Cash Out (Uang Keluar)")
        with st.form("cash_out_form"):
            kategori_out = st.selectbox("Pilih Kategori", ["KAS", "Expense", "Spending"])
            nominal_out = st.number_input("Nominal Pengeluaran (Rp)", min_value=0, value=0, step=10000, format="%d")
            catatan_out = st.text_input("Catatan Pengeluaran (Opsional)")
            submit_out = st.form_submit_button("Submit Cash Out")
            
            if submit_out:
                new_data = pd.DataFrame([{
                    "Tanggal": datetime.now(),
                    "Tipe": "Cash Out",
                    "Kategori": kategori_out,
                    "Nominal": int(nominal_out),
                    "Catatan": catatan_out
                }])
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Berhasil mencatat Cash Out: {kategori_out} sebesar {format_rupiah(nominal_out)}")
                st.rerun()

    # Fitur History & Hapus Spesifik
    st.divider()
    st.subheader("Riwayat Transaksi Hari Ini")
    df = pd.read_csv(DB_FILE)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    today = datetime.now().date()
    df_today = df[df['Tanggal'].dt.date == today].copy()
    
    if not df_today.empty:
        # Tampilkan dengan format Rupiah
        df_today['Nominal Display'] = df_today['Nominal'].apply(format_rupiah)
        st.dataframe(df_today[['Tanggal', 'Tipe', 'Kategori', 'Nominal Display', 'Catatan']], use_container_width=True, hide_index=True)
        
        st.write("**Hapus Transaksi (Tersinkron ke Sun Wealth & Equity):**")
        # Buat label untuk dropdown hapus
        df_today['Label'] = df_today.apply(lambda x: f"{x['Tanggal'].strftime('%H:%M')} - {x['Tipe']} - {x['Kategori']} - {format_rupiah(x['Nominal'])}", axis=1)
        
        selected_idx = st.selectbox("Pilih transaksi yang ingin dihapus", df_today.index, format_func=lambda i: df_today.loc[i, 'Label'])
        
        if st.button("Hapus Transaksi Terpilih", type="primary"):
            # PERBAIKAN UTAMA: Langsung menghapus berdasarkan Index baris di database asli
            df = df.drop(index=selected_idx)
            df.to_csv(DB_FILE, index=False)
            st.success("Transaksi berhasil dihapus dari database!")
            st.rerun()
    else:
        st.info("Belum ada transaksi hari ini.")