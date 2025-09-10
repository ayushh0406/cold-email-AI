import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    st.title("📧 Cold Mail Generator")
    st.write("Generate personalized cold emails from job postings automatically!")

    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ Instructions")
        st.markdown("""
        1. Paste the job posting URL.  
        2. Click **Submit**.  
        3. Get tailored cold emails with portfolio links.  
        """)

    # Input Section
    url_input = st.text_input("🔗 Enter a Job URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("🚀 Generate Email")

    if submit_button:
        if not url_input.startswith("http"):
            st.warning("⚠️ Please enter a valid URL.")
            return

        with st.spinner("🔎 Scraping job posting and generating email..."):
            try:
                # Load and clean job description
                loader = WebBaseLoader([url_input])
                data = loader.load().pop().page_content
                cleaned_data = clean_text(data)

                # Portfolio & job extraction
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(cleaned_data)

                if not jobs:
                    st.info("No jobs found on this page.")
                    return

                for idx, job in enumerate(jobs, start=1):
                    with st.expander(f"💼 Job {idx}: {job.get('title', 'Untitled')}"):
                        skills = job.get("skills", [])
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)

                        st.subheader("✉️ Generated Cold Email")
                        st.code(email, language="markdown")

                        if skills:
                            st.write("**Matched Skills:**", ", ".join(skills))
                        if links:
                            st.write("**Portfolio Links:**")
                            for link in links:
                                st.markdown(f"- [{link}]({link})")

            except Exception as e:
                st.error(f"❌ An error occurred:\n\n{str(e)}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
