import streamlit as st
from ProposalSkripsiByGemini import ProposalSkripsiByGemini
import os

def main():
    st.set_page_config(page_title="Proposal Skripsi Generator", page_icon="🎓", layout="wide")
    st.title("🎓 Proposal Skripsi Generator")
    st.write("Aplikasi ini menggunakan AI untuk membantu Anda membuat proposal skripsi berdasarkan penelitian sebelumnya.")

    # Sidebar for input fields
    st.sidebar.header("Pengaturan Proposal")
    judul_skripsi = st.sidebar.text_input("Judul Skripsi", "Analisis Sentimen Twitter")
    sejak_tahun = st.sidebar.number_input("Sejak Tahun (Opsional)", min_value=2000, max_value=2023, value=2018, step=1)
    api_key = st.sidebar.text_input("API Key Gemini", type="password")
    hasil_file = st.sidebar.text_input("Nama File Output", "skripsi.docx")

    # Initialize session state to track file creation
    if "files_generated" not in st.session_state:
        st.session_state.files_generated = False
        st.session_state.hasil_docx = None
        st.session_state.links_zip = None
        st.session_state.pdf_link_zip = None

    # Generate proposal when the button is clicked
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
                
                # Store files in session state
                st.session_state.files_generated = True
                st.session_state.hasil_docx = hasil_docx
                st.session_state.links_zip = links_zip
                st.session_state.pdf_link_zip = pdf_link_zip
                
                st.success("Proposal berhasil dibuat! Silakan unduh file di bawah ini.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

    # Display download buttons if files are generated
    if st.session_state.files_generated:
        st.subheader("Unduh Hasil")
        st.write("Klik tombol di bawah ini untuk mengunduh file hasil:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with open(st.session_state.hasil_docx, "rb") as file:
                st.download_button(
                    label="📄 Unduh Proposal Skripsi (DOCX)",
                    data=file,
                    file_name=hasil_file,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        with col2:
            with open(st.session_state.links_zip, "rb") as file:
                st.download_button(
                    label="📦 Unduh Semua Link (ZIP)",
                    data=file,
                    file_name="data_links_scholar.zip",
                    mime="application/zip"
                )
        with col3:
            with open(st.session_state.pdf_link_zip, "rb") as file:
                st.download_button(
                    label="📦 Unduh Semua PDF (ZIP)",
                    data=file,
                    file_name="pdf_files.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
