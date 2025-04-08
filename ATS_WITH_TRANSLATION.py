
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import pdfplumber
from googletrans import Translator  # Import Google Translator
from langdetect import detect  # Import language detection
from dotenv import load_dotenv
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import openai
import io
import pdf2image
import base64
from PIL import Image
import pdfplumber


# os.environ["OPENAI_API_KEY"]=grishu_opeanai_key
#
# Function to extract text from PDF using pdfplumber (for all pages)
def extract_text_from_pdf_plumber(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to get OpenAI response using ChatOpenAI from LangChain
def get_openai_response(input_text, resume_text, prompt):
    # Initialize the ChatOpenAI model
    chat = ChatOpenAI(model_name="gpt-4", temperature=0.2)

    # Send the job description, resume text, and prompt to OpenAI model
    response = chat([
        HumanMessage(content=input_text),  # Job description prompt
        HumanMessage(content=f"Resume Text: {resume_text}"),  # Extracted text from resume
        HumanMessage(content=prompt)  # Evaluation or scoring prompt
    ])

    return response.content

# Function to translate text into English using Google Translate
from deep_translator import GoogleTranslator

def translate_to_english(text):
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    return translated_text

# Function to detect if the language is not English
def detect_language(text):
    language = detect(text)
    return language != 'en'  # Returns True if the language is not English

# Streamlit app setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input fields
input_text = st.text_area("Job Description: ", key="input")  # Text area for job description
uploaded_file_job_desc = st.file_uploader("Upload Job Description (Optional)...", type=["txt", "pdf"])  # Option to upload job description

# File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches 
the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
"""

# Handling the responses based on button clicks
if submit1:
    if uploaded_file is not None:
        # Extract text from the full resume PDF
        resume_text = extract_text_from_pdf_plumber(uploaded_file)

        # Check if job description was uploaded as a file or input as text
        if uploaded_file_job_desc is not None:
            if uploaded_file_job_desc.name.endswith('.pdf'):
                # Extract job description from the PDF file
                job_desc_text = extract_text_from_pdf_plumber(uploaded_file_job_desc)
            elif uploaded_file_job_desc.name.endswith('.txt'):
                # Read text job description from the file
                job_desc_text = uploaded_file_job_desc.read().decode("utf-8")
            else:
                job_desc_text = input_text  # Default to the text area input
        else:
            job_desc_text = input_text  # Default to the text area input

        # Check if the job description is not in English and translate if necessary
        if detect_language(job_desc_text):
            job_desc_text_translated = translate_to_english(job_desc_text)
        else:
            job_desc_text_translated = job_desc_text  # No need to translate if already in English

        # Get the OpenAI response based on the translated job description and resume
        response = get_openai_response(job_desc_text_translated, resume_text, input_prompt1)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        # Extract text from the full resume PDF
        resume_text = extract_text_from_pdf_plumber(uploaded_file)

        # Check if job description was uploaded as a file or input as text
        if uploaded_file_job_desc is not None:
            if uploaded_file_job_desc.name.endswith('.pdf'):
                # Extract job description from the PDF file
                job_desc_text = extract_text_from_pdf_plumber(uploaded_file_job_desc)
            elif uploaded_file_job_desc.name.endswith('.txt'):
                # Read text job description from the file
                job_desc_text = uploaded_file_job_desc.read().decode("utf-8")
            else:
                job_desc_text = input_text  # Default to the text area input
        else:
            job_desc_text = input_text  # Default to the text area input

        # Check if the job description is not in English and translate if necessary
        if detect_language(job_desc_text):
            job_desc_text_translated = translate_to_english(job_desc_text)
        else:
            job_desc_text_translated = job_desc_text  # No need to translate if already in English

        # Get the OpenAI response for percentage match
        response = get_openai_response(job_desc_text_translated, resume_text, input_prompt3)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
