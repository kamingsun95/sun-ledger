import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

DB_FILE = "sun_ledger_data.csv"

def run():
    st.title("📊 Sun Wealth")
    st.write("Rekapitulasi keuangan bulanan Anda.")
    
    if not os.path.exists(DB_FILE):
        st.warning("Belum ada data transaksi.")
        return

    df = pd.read_csv(DB_FILE)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    
    # Filter bulan ini
    current_month = datetime.now().month
    current_year = datetime.now().year
    df_bulan_ini = df[(df['Tanggal'].dt.month == current_month) & (df['Tanggal'].dt.year == current_year)]
    
    total_in = df_bulan_ini[df_bulan_ini['Tipe'] == 'Cash In']['Nominal'].sum()
    total_out = df_bulan_ini[df_bulan_ini['Tipe'] == 'Cash Out']['Nominal'].sum()
    revenue = total_in - total_out
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cash Inflow", f"Rp {total_in:,.0f}".replace(",", "."))
    with col2:
        st.metric("Cash Outflow", f"Rp {total_out:,.0f}".replace(",", "."))
    with col3:
        st.metric("Revenue", f"Rp {revenue:,.0f}".replace(",", "."))
        
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Grafik Cash Inflow")
        df_in = df_bulan_ini[df_bulan_ini['Tipe'] == 'Cash In']
        if not df_in.empty:
            fig_in = px.pie(df_in, values='Nominal', names='Kategori', title='Pemasukan per Paket')
            st.plotly_chart(fig_in, use_container_width=True)
        else:
            st.info("Belum ada Cash In bulan ini.")
            
    with col_chart2:
        st.subheader("Grafik Cash Outflow")
        df_out = df_bulan_ini[df_bulan_ini['Tipe'] == 'Cash Out']
        if not df_out.empty:
            fig_out = px.pie(df_out, values='Nominal', names='Kategori', title='Pengeluaran per Kategori')
            st.plotly_chart(fig_out, use_container_width=True)
        else:
            st.info("Belum ada Cash Out bulan ini.")
            
    st.divider()
    st.subheader("Grafik Perbandingan Revenue (Inflow vs Outflow)")
    df_compare = pd.DataFrame({
        'Tipe': ['Cash Inflow', 'Cash Outflow'],
        'Nominal': [total_in, total_out]
    })
    fig_bar = px.bar(df_compare, x='Tipe', y='Nominal', color='Tipe', title='Perbandingan Inflow vs Outflow')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    st.subheader("Riwayat Bulan Sebelumnya")
    # Grouping by Month-Year
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)
    df_monthly = df.groupby(['Bulan', 'Tipe'])['Nominal'].sum().unstack(fill_value=0)
    if 'Cash In' not in df_monthly.columns: df_monthly['Cash In'] = 0
    if 'Cash Out' not in df_monthly.columns: df_monthly['Cash Out'] = 0
    df_monthly['Revenue'] = df_monthly['Cash In'] - df_monthly['Cash Out']
    st.dataframe(df_monthly.style.format("{:,.0f}".replace(",", ".")), use_container_width=True)
    
    # Tombol Export
    st.download_button("Export ke CSV", df.to_csv(index=False), "sun_ledger_report.csv")