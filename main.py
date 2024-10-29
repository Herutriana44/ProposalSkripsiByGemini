import streamlit as st
from ProposalSkripsiByGemini import ProposalSkripsiByGemini
import os

def main():
    st.set_page_config(page_title="Proposal Skripsi Generator", page_icon="🎓", layout="wide")
    st.title("🎓 Proposal Skripsi Generator")
    st.write("Aplikasi ini menggunakan AI untuk membantu Anda membuat proposal skripsi berdasarkan penelitian sebelumnya.")

    st.sidebar.header("Pengaturan Proposal")
    judul_skripsi = st.sidebar.text_input("Judul Skripsi", "Analisis Sentimen Twitter")
    sejak_tahun = st.sidebar.number_input("Sejak Tahun (Opsional)", min_value=2000, max_value=2023, value=2018, step=1)
    api_key = st.sidebar.text_input("API Key Gemini", type="password")
    hasil_file = st.sidebar.text_input("Nama File Output", "skripsi.docx")

    if st.sidebar.button("Buat Proposal"):
        if not api_key.strip():
            st.sidebar.error("API Key diperlukan untuk melanjutkan.")
        else:
            st.info("Mempersiapkan pembuatan proposal...")

            proposal_generator = ProposalSkripsiByGemini(
                judul_skripsi=judul_skripsi, 
                sejak_tahun=sejak_tahun, 
                api_key=api_key, 
                hasil_file=hasil_file
            )

            try:
                with st.spinner("Mengumpulkan data dan menghasilkan proposal..."):
                    hasil_docx, links_zip, pdf_link_zip = proposal_generator.run()
                st.success("Proposal berhasil dibuat!")

                st.subheader("Unduh Hasil")
                st.write("Klik tombol di bawah ini untuk mengunduh file hasil:")

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    with open(hasil_docx, "rb") as file:
                        st.download_button(
                            label="📄 Unduh Proposal Skripsi (DOCX)",
                            data=file,
                            file_name=hasil_file,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                with col2:
                    with open(links_zip, "rb") as file:
                        st.download_button(
                            label="📦 Unduh Semua Link (ZIP)",
                            data=file,
                            file_name="links.zip",
                            mime="application/zip"
                        )
                with col3:
                    with open(pdf_link_zip, "rb") as file:
                        st.download_button(
                            label="📦 Unduh Semua PDF (ZIP)",
                            data=file,
                            file_name="pdf_files.zip",
                            mime="application/zip"
                        )

            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
