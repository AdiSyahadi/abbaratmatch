import streamlit as st
import pandas as pd

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
        
        # Daftar nomor invoice yang tidak cocok/tidak ada
        unmatched_invoices = deleted_df['Invoice'].unique().tolist()
        
        # Hitung jumlah nomor invoice yang tidak cocok
        unmatched_count = len(unmatched_invoices)
        
        # Temukan nomor invoice dalam file daftar valid yang tidak digunakan dalam file rekap
        unused_invoices = [inv for inv in valid_invoices if inv not in df_rekap['Invoice'].unique()]
        
        # Tampilkan jumlah baris sebelum dan sesudah filter
        st.write(f"Jumlah baris sebelum filter: {len(df_rekap)}")
        st.write(f"Jumlah data program abbarat: {len(filtered_df)}")
        st.write(f"Jumlah data program pusat: {len(deleted_df)}")
        #st.write(f"Jumlah nomor invoice yang tidak cocok: {unmatched_count}")
        
        # Tampilkan daftar nomor invoice yang tidak cocok
        #st.write("Daftar Nomor Invoice yang Tidak Cocok/Tidak Ada:")
        #st.write(unmatched_invoices)
        
        # Tampilkan daftar nomor invoice dalam file daftar valid yang tidak digunakan
        #st.write("Nomor Invoice dalam File Daftar Valid yang Tidak Digunakan:")
        #st.write(unused_invoices)
        
        # Tampilkan data hasil filter
        st.write("Data program ab barat (Valid):")
        st.dataframe(filtered_df)
        
        # Tampilkan data yang dihapus
        st.write("Data program laz pusat (Invalid):")
        st.dataframe(deleted_df)

        # Tampilkan data yang dihapus
        st.write("Data Invoice web yang tidak cocok (Invalid):")
        st.dataframe(unused_invoices)
        
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
        if st.button("Download Daftar Nomor Invoice Flip Tidak Cocok"):
            # Buat DataFrame untuk nomor invoice yang tidak cocok
            unmatched_df = pd.DataFrame({"Nomor Invoice Tidak Cocok": unmatched_invoices})
            output_unmatched_file = "unmatched_invoices.xlsx"
            unmatched_df.to_excel(output_unmatched_file, index=False)
            st.success(f"File daftar nomor invoice yang tidak cocok berhasil disimpan sebagai {output_unmatched_file}")
        
        # Download daftar nomor invoice dalam file daftar valid yang tidak digunakan
        if st.button("Download Daftar Nomor Invoice WEB Tidak Cocok"):
            # Buat DataFrame untuk nomor invoice yang tidak digunakan
            unused_df = pd.DataFrame({"Nomor Invoice Tidak Digunakan": unused_invoices})
            output_unused_file = "unused_invoices.xlsx"
            unused_df.to_excel(output_unused_file, index=False)
            st.success(f"File daftar nomor invoice yang tidak digunakan berhasil disimpan sebagai {output_unused_file}")
