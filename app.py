import streamlit as st
from dotenv import load_dotenv
from modules.llm_setup import setup_llm
from modules.job_extractor import extract_job_data
from modules.vector_db import setup_vector_db, get_relevant_portfolio
from modules.email_generator import generate_email
from modules.config import Config

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="Generic Cold Email Generator", layout="wide")

    st.markdown(
        """
        <style>
        .main {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f5;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Generic Cold Email Generator")
    st.write("Generate a targeted cold email for various purposes")

    with st.sidebar:
        st.header("Configuration")
        user_name = st.text_input("Your Name", "Himanshu Sharma")
        company_name = st.text_input("Company Name", "Recruitify")
        position = st.text_input("Position", "Business Development Executive")
        company_description = st.text_area("Company Description", "AI & Software Consulting company dedicated to facilitating the seamless integration of business processes through automated tools.")
        intention = st.text_area("Intention", "To provide tailored solutions for scalability, process optimization, cost reduction, and heightened overall efficiency.")
        email_purpose = st.text_area("Email Purpose", "Discussing potential collaboration opportunities")

        config = Config(company_name, position, company_description, intention, email_purpose).get_config()

    job_url = st.text_input("Job Posting URL or Relevant Information", "https://jobs.nike.com/job/R-40715")

    if st.button("Generate Email"):
        with st.spinner("Processing..."):
            llm = setup_llm()
            job_info = extract_job_data(job_url, llm)

            if job_info:
                st.subheader("Extracted Information")
                st.json(job_info)

                job_skills = ""
                if "skill" in job_info and job_info["skill"]:
                    if isinstance(job_info["skill"], list):
                        job_skills = ", ".join(job_info["skill"])
                    elif isinstance(job_info["skill"], str):
                        job_skills = job_info["skill"]

                collection = setup_vector_db()
                portfolio_links = get_relevant_portfolio(job_skills, collection)

                email_content = generate_email(job_info, portfolio_links, user_name, llm, config)

                st.subheader("Generated Cold Email")
                st.markdown(email_content, unsafe_allow_html=True)

                st.text_area("Copy Email", email_content, height=300)

    st.divider()
    st.markdown("Developed by Himanshu Sharma")

if __name__ == "__main__":
    main()
