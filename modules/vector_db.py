import os
import streamlit as st
import chromadb
import uuid
import pandas as pd

def setup_vector_db():
    """
    Set up ChromaDB for portfolio storage.
    """
    data_dir = "vectorstore"
    os.makedirs(data_dir, exist_ok=True)

    client = chromadb.PersistentClient(data_dir)
    collection = client.get_or_create_collection(name="portfolio")

    # Load portfolio data if the collection is empty
    if not collection.count():
        try:
            df = pd.read_csv("data/my_portfolio.csv")
            for _, row in df.iterrows():
                collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"], "title": row["Title"]},  # Include title for better link display
                    ids=[str(uuid.uuid4())]
                )
            st.success("Portfolio data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading portfolio: {e}")

    return collection

def get_relevant_portfolio(job_skills, collection):
    """
    Query the vector database for relevant portfolio items.
    """
    try:
        st.write("Job skills for search:", job_skills)
        st.write("Collection count:", collection.count())

        if not job_skills:
            st.warning("No skills provided for portfolio matching")
            return []

        try:
            query_results = collection.query(
                query_texts=job_skills,
                n_results=min(2, collection.count())
            )

            st.write("Raw query results:", query_results)

            if 'metadatas' in query_results:
                return query_results['metadatas']
            else:
                st.warning("No metadatas found in query results")
                return []

        except Exception as query_error:
            st.error(f"Error during query execution: {query_error}")
            return []

    except Exception as e:
        st.error(f"Error in portfolio retrieval: {e}")
        return []
