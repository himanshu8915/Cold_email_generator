import requests
from bs4 import BeautifulSoup
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st

def extract_job_data(url, llm):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        page_data = soup.get_text(separator=' ', strip=True)

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job posting details and return them in JSON format containing
            the following keys: 'role', 'experience', 'skill', and 'description'.
            Only return the valid JSON.

            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | llm
        res = chain_extract.invoke({"page_data": page_data})

        json_parser = JsonOutputParser()
        try:
            job_info = json_parser.parse(res.content)
            return job_info
        except Exception as e:
            st.error(f"Error parsing JSON: {e}")
            return None

    except Exception as e:
        st.error(f"Error extracting job data: {e}")
        return None
