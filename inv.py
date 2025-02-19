import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # Impor Matplotlib

# Judul aplikasi
st.title("Filter Data Berdasarkan Nomor Invoice dari CSV")

# Upload file Excel rekap
uploaded_rekap_file = st.file_uploader("Upload File Excel dari FLIP", type=["xlsx"])

# Upload file CSV nomor invoice valid
uploaded_invoice_file = st.file_uploader("Upload File CSV Nomor Invoice dari Website", type=["csv"])

if uploaded_rekap_file is not None and uploaded_invoice_file is not None:
    # Baca file Excel rekap
    df_rekap = pd.read_excel(uploaded_rekap_file)
    
    # Baca file CSV nomor invoice valid
    df_invoices = pd.read_csv(uploaded_invoice_file)
    
    # Membersihkan nama kolom file CSV (hapus spasi dan ubah ke lowercase)
    df_invoices.columns = df_invoices.columns.str.strip().str.lower()
    
    # Periksa apakah kolom 'invoice' ada
    if 'invoice' not in df_invoices.columns:
        st.error("Kolom 'invoice' tidak ditemukan dalam file CSV. Pastikan nama kolom benar.")
    else:
        # Konversi kolom invoice ke list dan bersihkan datanya
        valid_invoices = df_invoices['invoice'].str.strip().str.lower().tolist()
        
        # Fungsi untuk memisahkan nomor invoice dan judul program
        def split_invoice_and_title(full_title):
            if isinstance(full_title, str):  # Pastikan input adalah string
                parts = full_title.split(" ", 1)  # Pisahkan berdasarkan spasi pertama
                if len(parts) == 2:
                    return parts[0].strip().lower(), parts[1].strip()  # Kembalikan nomor invoice dan judul
                elif len(parts) == 1:
                    return parts[0].strip().lower(), ""  # Jika tidak ada judul, kembalikan string kosong
            return None, None  # Jika input bukan string, kembalikan None
        
        # Tambahkan kolom baru untuk nomor invoice dan judul program
        df_rekap[['Invoice', 'Judul Program']] = df_rekap['Judul Produk'].apply(
            lambda x: pd.Series(split_invoice_and_title(x))
        )
        
        # Filter data berdasarkan nomor invoice valid
        filtered_df = df_rekap[df_rekap['Invoice'].isin(valid_invoices)]
        
        # Filter data yang dihapus (invoice tidak valid)
        deleted_df = df_rekap[~df_rekap['Invoice'].isin(valid_invoices)]
        
        # Hitung jumlah nominal untuk data valid dan invalid
        try:
            total_nominal_valid = filtered_df['Nominal Settled (Rp)'].sum()
            total_nominal_invalid = deleted_df['Nominal Settled (Rp)'].sum()
        except KeyError:
            st.error("Kolom 'Nominal Settled (Rp)' tidak ditemukan dalam file Excel. Pastikan nama kolom benar.")
            total_nominal_valid = 0
            total_nominal_invalid = 0
        
        # Persiapkan data untuk pie chart
        categories = ["Program Abbarat", "Program Pusat"]
        values = [len(filtered_df), len(deleted_df)]
        colors = ["green", "yellow"]  # Warna untuk setiap bagian
        
        # Buat pie chart menggunakan Matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))  # Atur ukuran chart
        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title("Proporsi Data Program AB Barat dan AB Pusat")
        
        # Tampilkan pie chart di Streamlit
        st.write("Visualisasi Proporsi Data Program AB Barat dan AB Pusat:")
        st.pyplot(fig)
        
        # Tampilkan catatan total data dan nominal
        st.write(f"Catatan:")
        st.write(f"- Total Data: {len(df_rekap)}")
        st.write(f"- Program Abbarat :  {len(filtered_df)} (Total Nominal: Rp{total_nominal_valid:,.0f})")
        st.write(f"- Program Pusat :  {len(deleted_df)} (Total Nominal: Rp{total_nominal_invalid:,.0f})")
        
        # Tampilkan data hasil filter
        st.write("Data Hasil Filter (Valid):")
        st.dataframe(filtered_df)
        
        # Tampilkan data yang dihapus
        st.write("Data yang Dihapus (Invalid):")
        st.dataframe(deleted_df)
        
        # Download file hasil filter
        if st.button("Download File Hasil Filter"):
            output_file = "filtered_data.xlsx"
            filtered_df.to_excel(output_file, index=False)
            st.success(f"File hasil filter berhasil disimpan sebagai {output_file}")
        
        # Download file data yang dihapus
        if st.button("Download File Data transaksi laz pusat"):
            output_deleted_file = "deleted_data.xlsx"
            deleted_df.to_excel(output_deleted_file, index=False)
            st.success(f"File data yang dihapus berhasil disimpan sebagai {output_deleted_file}")
        
        # Download daftar nomor invoice yang tidak cocok
        unmatched_invoices = deleted_df['Invoice'].unique().tolist()
        if st.button("Download Daftar Nomor Invoice Flip Tidak Cocok"):
            unmatched_df = pd.DataFrame({"Nomor Invoice Tidak Cocok": unmatched_invoices})
            output_unmatched_file = "unmatched_invoices.xlsx"
            unmatched_df.to_excel(output_unmatched_file, index=False)
            st.success(f"File daftar nomor invoice yang tidak cocok berhasil disimpan sebagai {output_unmatched_file}")
        
        # Download daftar nomor invoice dalam file daftar valid yang tidak digunakan
        unused_invoices = [inv for inv in valid_invoices if inv not in df_rekap['Invoice'].unique()]
        if st.button("Download Daftar Nomor Invoice WEB Tidak Cocok"):
            unused_df = pd.DataFrame({"Nomor Invoice Tidak Digunakan": unused_invoices})
            output_unused_file = "unused_invoices.xlsx"
            unused_df.to_excel(output_unused_file, index=False)
            st.success(f"File daftar nomor invoice yang tidak digunakan berhasil disimpan sebagai {output_unused_file}")
