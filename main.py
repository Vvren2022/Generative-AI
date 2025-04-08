from dotenv import load_dotenv
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import io
import pdf2image
import base64
from PIL import Image
import pdfplumber
# Load environment variables
# os.environ["OPENAI_API_KEY"]=grishu_opeanai_key




# Extract text from PDF using PyPDF2 (for all pages)
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


# Streamlit app setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")
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
        # Extract text from the full PDF
        resume_text = extract_text_from_pdf_plumber(uploaded_file)
        response = get_openai_response(input_prompt1, resume_text, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        # Extract text from the full PDF
        resume_text = extract_text_from_pdf_plumber(uploaded_file)
        response = get_openai_response(input_prompt3, resume_text, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
