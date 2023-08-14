import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import zipfile
import os
import streamlit as st
import tempfile

# Function to process the Excel file
def process_excel(file):
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active

    # Check headings
    headings = ["Index", "PROBLEM", "RESEARCH", "SOLUTION", "KEYS TO SUCCESS"]
    for idx, heading in enumerate(headings):
        assert sheet.cell(row=1, column=idx+1).value == heading, f"Expected {heading}, but found {sheet.cell(row=1, column=idx+1).value}"

    # Temporary directory to store the PDFs
    with tempfile.TemporaryDirectory() as pdf_dir:
        # Iterate through the rows, starting from the second row (indexing from 1)
        for row_idx in range(2, sheet.max_row + 1):
            index = sheet.cell(row=row_idx, column=1).value
            contents = [sheet.cell(row=row_idx, column=col_idx+1).value for col_idx in range(1, len(headings))]

            # Create PDF file
            pdf_file = f"{pdf_dir}/Entry_{index}.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter
            
            # Entry number
            c.drawString(100, height - 80, f"Entry# {index}")
            
            # Add contents to the PDF
            for idx, content in enumerate(contents):
                c.drawString(100, height - 120 - (idx * 70), f"{headings[idx+1]}:")
                c.drawString(100, height - 140 - (idx * 70), str(content))


            # Add the scoring section
            c.drawString(100, height - 320, "SCORING")
            c.drawString(100, height - 340, "Research ______/30pts max")
            c.drawString(100, height - 360, "Solution ______/40pts max")
            c.drawString(100, height - 380, "Uniqueness ______/20pts max")
            c.drawString(100, height - 400, "Professionalism ______/10pts max")
            c.drawString(100, height - 420, "Total Score: ___________")
            c.drawString(100, height - 440, "NOTES:")

            # Save the PDF file
            c.save()

        # Create a ZIP file with the PDFs
        zip_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for root, _, files in os.walk(pdf_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        return zip_file.name

# Streamlit app
st.title("Excel to PDF Converter")

uploaded_file = st.file_uploader("Drag and drop your Excel file here:", type=["xlsx"])

if uploaded_file is not None:
    with st.spinner("Processing..."):
        zip_path = process_excel(uploaded_file)
    st.success("Processing complete!")
    
    # Serve the ZIP file for download
    with open(zip_path, 'rb') as file:
        zip_bytes = file.read()
        st.download_button(
            label="Download ZIP file",
            data=zip_bytes,
            file_name="entries.zip",
            mime="application/zip",
        )

