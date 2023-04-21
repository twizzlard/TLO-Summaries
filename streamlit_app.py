import streamlit as st
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re
import pandas as pd

st.title('PDF Processor')
uploaded_file = st.file_uploader('Upload a PDF file', type='pdf')

if uploaded_file is not None:
    # Process the PDF file
    df = process_pdf(uploaded_file)
    
    # Display the DataFrame
    st.write(df)
    
    # Offer a download link for the CSV file
    st.markdown('### Download CSV')
    st.markdown(get_download_link(df), unsafe_allow_html=True)
