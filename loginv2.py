import streamlit as st
import gnupg

# Inisialisasi GPG
gpg = gnupg.GPG()

# Upload kunci publik PGP
st.title('Enkripsi Pesan Menggunakan PGP')
public_key = st.text_area('Masukkan Kunci Publik Penerima', '')

# Teks yang ingin dienkripsi
message = st.text_area('Masukkan Teks yang Akan Dikirim', '')

if st.button('Enkripsi'):
    if public_key and message:
        # Impor kunci publik
        import_result = gpg.import_keys(public_key)
        if import_result.count == 0:
            st.error('Kunci publik tidak valid')
        else:
            # Enkripsi pesan
            encrypted_message = gpg.encrypt(message, import_result.fingerprints[0])
            if encrypted_message.ok:
                st.subheader('Pesan yang Terenkripsi:')
                st.text(encrypted_message)
            else:
                st.error('Terjadi kesalahan saat enkripsi')
    else:
        st.error('Pastikan untuk mengisi kunci publik dan pesan.')
