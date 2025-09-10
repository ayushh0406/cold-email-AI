import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv", persist_dir="vectorstore"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """Loads portfolio data into ChromaDB if not already loaded."""
        if self.collection.count() == 0:
            records = []
            for _, row in self.data.iterrows():
                records.append({
                    "documents": row["Techstack"],
                    "metadatas": {"links": row["Links"]},
                    "ids": str(uuid.uuid4())
                })

            self.collection.add(
                documents=[r["documents"] for r in records],
                metadatas=[r["metadatas"] for r in records],
                ids=[r["ids"] for r in records]
            )

    def query_links(self, skills, n_results=2):
        """
        Queries portfolio based on given skills.
        Returns a flat list of links instead of raw Chroma metadata.
        """
        if not skills:
            return []

        results = self.collection.query(
            query_texts=skills,
            n_results=n_results
        )

        metadatas = results.get("metadatas", [])
        # Flatten list of dicts and return only links
        links = [meta["links"] for group in metadatas for meta in group if "links" in meta]
        return list(set(links))  # remove duplicates
