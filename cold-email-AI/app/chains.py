import os
from typing import List, Dict, Union
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


class Chain:
    def __init__(self, model_name: str = "llama-3.1-70b-versatile", temperature: float = 0):
        """Initialize Chain with Groq LLM client."""
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise EnvironmentError("GROQ_API_KEY not found. Please set it in your .env file.")

        self.llm = ChatGroq(
            temperature=temperature,
            groq_api_key=groq_api_key,
            model_name=model_name
        )
        self.json_parser = JsonOutputParser()

        # Predefined prompts (so they’re reused, not re-created every call)
        self.prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            Extract all job postings in JSON array format.
            Each job must include:
            - role
            - experience
            - skills
            - description

            Rules:
            - Strictly return valid JSON only.
            - No commentary or extra text.

            ### JSON OUTPUT:
            """
        )
        self.prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are **Mohan**, BDE at **AtliQ**.  
            AtliQ delivers AI & Software Consulting solutions that drive:
            - Business process automation
            - Scalable and optimized workflows
            - Cost efficiency

            Write a cold email to the client describing how AtliQ can help.  
            Use relevant portfolio links: {link_list}  

            Rules:
            - Output only the email body (no preamble).
            - Keep tone professional and concise.
            - End with a polite CTA.

            ### EMAIL:
            """
        )

    def extract_jobs(self, cleaned_text: str, chunk_size: int = 4000) -> List[Dict]:
        """
        Extract structured job postings from scraped text.
        Handles long text by chunking and retrying.
        """
        if not cleaned_text.strip():
            return []

        jobs = []
        chunks = [cleaned_text[i:i + chunk_size] for i in range(0, len(cleaned_text), chunk_size)]

        for chunk in chunks:
            chain_extract = self.prompt_extract | self.llm
            res = chain_extract.invoke({"page_data": chunk})

            try:
                parsed = self.json_parser.parse(res.content)
                jobs.extend(parsed if isinstance(parsed, list) else [parsed])
            except OutputParserException:
                # Skip bad chunk but continue processing others
                continue

        return jobs

    def write_mail(self, job: Dict, links: Union[List[str], None]) -> str:
        """Generate a cold email for a given job and portfolio links."""
        chain_email = self.prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": ", ".join(links) if links else "No relevant portfolio links"
        })
        return res.content.strip()


if __name__ == "__main__":
    try:
        chain = Chain()
        print("✅ Chain initialized successfully with Groq API.")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
