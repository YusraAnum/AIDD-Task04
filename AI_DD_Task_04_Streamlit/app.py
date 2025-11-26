
import streamlit as st
import io
from pdf_summarizer import summarize_pdf_text
from quiz_generator import generate_quiz
from utils import extract_text_from_pdf # Assuming utils.py has this function

st.set_page_config(layout="wide", page_title="Gemini AI Tools")

st.title("Gemini AI Powered PDF Tools")

# --- Tabs ---
tab1, tab2 = st.tabs(["PDF Summarizer", "Quiz Generator"])

with tab1:
    st.header("Summarize your PDF Document")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    pdf_text_input = st.text_area(
        "Or paste your text here (if no PDF uploaded)", 
        height=300
    )

    extracted_or_input_text = ""
    if uploaded_file:
        try:
            initial_extracted_text = extract_text_from_pdf(uploaded_file)
            st.success("Text extracted from PDF successfully!")
            # Use st.session_state to allow editing and retain value
            if "pdf_extracted_text_area" not in st.session_state or st.session_state["pdf_extracted_text_area"] != initial_extracted_text:
                st.session_state["pdf_extracted_text_area"] = initial_extracted_text
            
            extracted_or_input_text = st.text_area("Extracted Text (you can edit this)", key="pdf_extracted_text_area", height=300)

        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            st.session_state["pdf_extracted_text_area"] = ""
    elif pdf_text_input:
        extracted_or_input_text = pdf_text_input
        if "pdf_extracted_text_area" in st.session_state:
            del st.session_state["pdf_extracted_text_area"] # Clear if previous PDF was there
            
    if st.button("Summarize"):
        text_to_summarize = ""
        if uploaded_file and "pdf_extracted_text_area" in st.session_state:
            text_to_summarize = st.session_state["pdf_extracted_text_area"]
        elif pdf_text_input:
            text_to_summarize = pdf_text_input
        
        if text_to_summarize:
            with st.spinner("Summarizing..."):
                summary = summarize_pdf_text(text_to_summarize)
                st.subheader("Summary")
                st.write(summary)
        else:
            st.warning("Please upload a PDF or paste some text to summarize.")

with tab2:
    st.header("Generate Quizzes from Text")

    quiz_source_text = st.text_area(
        "Paste text here to generate quiz questions", 
        height=300, 
        key="quiz_text_input"
    )

    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input(
            "Number of Questions", 
            min_value=1, 
            max_value=20, 
            value=5, 
            step=1
        )
    with col2:
        quiz_type = st.selectbox(
            "Question Type", 
            ["MCQ", "True/False", "Open-ended"]
        )

    if st.button("Generate Quiz"):
        if quiz_source_text:
            with st.spinner("Generating quiz..."):
                quiz = generate_quiz(quiz_source_text, num_questions, quiz_type)
                st.subheader("Generated Quiz")
                st.write(quiz)
        else:
            st.warning("Please paste some text to generate a quiz.")

