import json
from typing import List
from dataclasses import asdict
from doc_processor import DocProcessor
from data_extractor import DataExtractor
from section_summarizer import SectionSummarizer
from vector_embedder import VectorEmbedder
from company_data_class import CompanyData, DocumentData


class Pipeline:
    def __init__(self, pdf_folder_path: str, structured_json_path: str, final_output_json_path: str,
                 vector_store: str):
        self.pdf_folder = pdf_folder_path
        self.structured_json = structured_json_path
        self.final_output_json = final_output_json_path
        self.vector_store_name = vector_store

    def process_pdfs(self):
        dp = DocProcessor(folder_path=self.pdf_folder, output_path=self.structured_json)
        docs = dp.get_processed_docs()
        dp.store_output()
        return docs

    @staticmethod
    def extract_company_data(docs: List[DocumentData]):
        companies = []

        for doc in docs:
            company_data = DataExtractor.get_company_data(doc)
            companies.append(company_data)
        return companies

    @staticmethod
    def summarize_company_sections(companies_data: List[CompanyData]) -> List[CompanyData]:
        summarizer = SectionSummarizer()
        for company in companies_data:
            summarizer.summarize_sections(company)
        return companies_data

    def run_pipeline(self) -> (List[CompanyData], any, list):
        print("Starting pipeline execution...")

        docs = self.process_pdfs()
        print(f"Processed PDFs: {len(docs)} documents extracted.")

        company_data = self.extract_company_data(docs)
        print(f"Extracted company data for {len(company_data)} companies.")
        company_data = self.summarize_company_sections(company_data)
        print("Summarized company sections.")

        vector_embedder = VectorEmbedder()
        print("Initialized VectorEmbedder.")

        vector_embedder.store_embeddings(company_data, self.vector_store_name)
        print(f"Stored embeddings in vector store")
        companies_as_dict = [asdict(company) for company in company_data]
        with open(self.final_output_json, "w", encoding="utf-8") as f:
            json.dump(companies_as_dict, f, indent=2)
        print(f"Stored company data to {self.final_output_json}")

        print("Pipeline execution completed.")
        return company_data


if __name__ == "__main__":
    pdf_folder = "docs"
    structured_json = "structured.json"
    final_output_json = "company_data.json"
    vector_store_name = "vector_store"
    pipeline = Pipeline(pdf_folder, structured_json, final_output_json, vector_store_name)
    companies = pipeline.run_pipeline()

