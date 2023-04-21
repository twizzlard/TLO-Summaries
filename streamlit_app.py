import streamlit as st
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re
import pandas as pd

def whichHeading(heading, content):
    if heading == 'General Information':
        getGenInfo(content)
    elif heading == 'Next Up':
        getNextUp(content)
    elif heading == 'Notes':
        getNotes(content)
    elif heading == 'Client Case Policies':
        getClientPolicies(content)
    elif heading == 'Property Information':
        getPropertyInfo(content)
    elif heading == 'Vehicle Information':
        getVehicleInfo(content)
    elif heading == 'Subject Information':
        getSubjectInfo(content)
    elif heading == 'Employer Information':
        getEmployerInfo(content)
    else:
        print('Unrecognized heading:', heading)
        
        
def getNextUp(section):
    
    secheadings = ['Next Task Due Date', 'Next Task Due', 'Subject:', 'Assigned To:']
    
    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getGenInfo(section):
    
    secheadings = ['Created On:', 'Due Date:', 'Referral:', 'Client:', 'Client Contact:', 'Case Type:',
                   'Case Services:', 'Company Location:', 'Case Region:', 'Case Location:', 'Case Number:',
                   'Claim Number:', 'SIU Number:',
                   'Case Manager:', 'Investigator:', 'Salesperson:']
    
    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
        
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getNotes(section):
    
    secheadings = ['Admin Notes:', 'Scheduling Notes:', 'Notes & Instructions:']

    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getClientPolicies(section):
    # Get Client Case Policies section

    field01 = section
    fields = [field01]
    fields = [x.strip() for x in fields]
    fields

    df = pd.DataFrame(fields)
    df.index = ['Client Case Policies']

    dfList.append(df)
    return df

def getSubjectInfo(section):
    
    secheadings = ['Full Name:', 'Alias:', 'Date of Birth:', 'SSN:', 'Home Phone:', 'Cell Phone:',
                   'Sex:', 'Race:', 'Height:', 'Weight:', 'Hair:', 'Build:', 'Eyes:', 'Glasses:',
                   'Spouse:', 'Children:', 'Other Characteristics:', 'Drivers License\nNumber / State:',
                   'Date of Injury:', 'Notes:', 'Injury / Limitations:', 'Street Address:'
                  ]

    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
            
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    field = ['Subject_' + x for x in field]
    
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getEmployerInfo(section):
    # Get Employer Information section
    
    secheadings = ['Name:', 'Occupation:', 'Is the Insured\?:', 'Ok to Contact\?:', 'Primary Contact:',
                   'Secondary Contact:', 'Office phone:', 'Alternate Phone:', 'Fax:', 'Street Address:',
                   'Notes:'
                  ]    

    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    field = ['Employer_' + x for x in field]
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getVehicleInfo(section):
    # Get Vehicle Information section

    secheadings = ['Name:', 'Year:', 'Color:', 'Make:', 'Model:', 'Tag:', 'State/Province:', 
                   'Registered To:', 'Notes:',
                  ]    

    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    field = ['Vehicle_' + x for x in field]
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def getPropertyInfo(section):
    # Get Property Information section

    secheadings = ['Name:', 'Street Address:', 'Notes:'
                  ]    

    pattern = '|'.join(secheadings)

    fieldcontent = re.split(pattern, section)[1:]
    
    field = re.findall(pattern, section)
    field = [x.strip() for x in field]
    field = ['Property_' + x for x in field]
    
    df = pd.DataFrame(fieldcontent, field)
    dfList.append(df)
    return df

def process_pdf(uploaded_file):

    # Open the PDF file in read binary mode
#     pdf_file = open(uploaded_file, 'rb')
    pdf_file = uploaded_file

    # Create a PDF resource manager object
    resource_manager = PDFResourceManager()

    # Create a file-like buffer to receive the text
    text_buffer = io.StringIO()

    # Create a text converter object
    text_converter = TextConverter(resource_manager, text_buffer, laparams=LAParams())

    # Create a PDF interpreter object
    pdf_interpreter = PDFPageInterpreter(resource_manager, text_converter)

    # Loop through each page in the PDF file
    for page in PDFPage.get_pages(pdf_file):
        # Process the current page
        pdf_interpreter.process_page(page)

    # Get the text from the buffer
    text = text_buffer.getvalue()
    text = text.replace('\x0c','')
    text = text.replace('Quick Links\nView related case updates\nView related events/tasks\nView similar subjects','')
    text = text.replace('Photo','')

    # Close the buffer and the PDF file
    text_buffer.close()
    pdf_file.close()

    # Print the extracted text
    print(text[:100])

    headings = ['Next Up', 'General Information', 'Notes', 'Client Case Policies', 'Property Information',
                'Vehicle Information', 'Subject Information', 'Employer Information', 'Connections', 'Current Status']

    pattern = '\n|\n'.join(headings)

    sections = re.split(pattern, text)[1:]
    sectionheadings = re.findall(pattern, text)
    sectionheadings = [x.strip() for x in sectionheadings]

    # for i in range(len(sections)):
    #     print(f"Section {i+1}: {sectionheadings[i]}")
    #     print(sections[i])


    dfSections = pd.DataFrame(sections, sectionheadings)
    dfSections = dfSections.reset_index()
    dfSections.columns = ['Heading', 'Content']

    dfList = []

    # Get doc number and doc creation time

    field01 = re.search('([A-Z0-9\-]+) \(This document was generated on: (\d+/\d+/\d{2} \d+:\d{2} (?:AM|PM))\)', 
                        text, flags=re.DOTALL)[1]
    field02 = re.search('([A-Z0-9\-]+) \(This document was generated on: (\d+/\d+/\d{2} \d+:\d{2} (?:AM|PM))\)', 
                        text, flags=re.DOTALL)[2]

    fields = [field01, field02]

    fields = [x.strip() for x in fields]
    fields

    df = pd.DataFrame(fields)

    df.index = ['Document Number', 'Document Creation Date/Time'
               ]

    dfList.append(df)
    
    df = pd.concat(dfList)
    
    df[0] = df[0].str.strip()
    
    df = df.T
    
    df.to_csv('Summary Output TrackOps Demo.csv', index=False)
    
    return df

st.title('PDF Processor')
uploaded_file = st.file_uploader('Upload a PDF file', type='pdf')

if uploaded_file is not None:
    uploaded_file = uploaded_file.read()
    # Process the PDF file
    df = process_pdf(uploaded_file)
    
    # Display the DataFrame
    st.write(df)
    
    # Offer a download link for the CSV file
    st.markdown('### Download CSV')
    st.markdown(get_download_link(df), unsafe_allow_html=True)
