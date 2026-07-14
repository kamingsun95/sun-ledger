import streamlit as st
import pandas as pd
import os

DB_FILE = "sun_ledger_data.csv"
INITIAL_LOSS = 299357000

def format_rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

def run():
    st.title("🛡️ Sun Equity & Recovery")
    st.write("Tracking pemulihan modal dan kerugian investasi.")
    
    if not os.path.exists(DB_FILE):
        st.warning("Belum ada data transaksi.")
        return

    df = pd.read_csv(DB_FILE)
    
    # HANYA menghitung Cash Out dengan kategori KAS yang mengurangi kerugian
    df_kas = df[(df['Tipe'] == 'Cash Out') & (df['Kategori'] == 'KAS')]
    total_setoran_kas = df_kas['Nominal'].sum()
    
    sisa_kerugian = max(0, INITIAL_LOSS - total_setoran_kas)
    persentase_recovery = (total_setoran_kas / INITIAL_LOSS) * 100 if INITIAL_LOSS > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Kerugian Awal", format_rupiah(INITIAL_LOSS))
        st.metric("Total Setoran KAS (Modal)", format_rupiah(total_setoran_kas))
        
    with col2:
        st.metric("Sisa Kerugian", format_rupiah(sisa_kerugian))
        st.metric("Progress Recovery", f"{persentase_recovery:.2f}%")
        
    st.divider()
    st.subheader("Progress Balik Modal")
    # Mengubah ke skala 0.0 - 1.0 untuk st.progress
    progress_value = min(persentase_recovery / 100, 1.0)
    st.progress(progress_value)
    
    if persentase_recovery >= 100:
        st.balloons()
        st.success("🎉 SELAMAT! Modal sudah kembali sepenuhnya (Break-even Point tercapai)!")
    else:
        st.info(f"Tinggal {format_rupiah(sisa_kerugian)} lagi untuk membalikkan modal. Tetap semangat!")