import os
import fitz
import json
from company_data_class import DocumentData
from dataclasses import asdict


class DocProcessor:
    def __init__(self, folder_path="", output_path=""):
        self.folder_path = folder_path
        self.output_path = output_path
        self.docs_data = []

    @staticmethod
    def extract_text_from_pdf(pdf_path) -> str:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text

    def process_files(self):
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.folder_path, filename)
                # print(f"Processing: {file_path}")
                text = self.extract_text_from_pdf(file_path)
                doc_data = DocumentData(
                    full_text=text,
                    file_path=file_path
                )
                self.docs_data.append(doc_data)

    def store_output(self, output_path: str = ""):
        if output_path:
            path = output_path
        else:
            path = self.output_path
        docs_dict = [asdict(doc) for doc in self.docs_data]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(docs_dict, f, indent=2)
        print(f"Structured data saved to {path}")

    def get_processed_docs(self):
        if not self.docs_data:
            self.process_files()
            return self.docs_data
        else:
            return self.docs_data

    def set_folder_path(self, folder_path: str):
        self.folder_path = folder_path

    def set_output_path(self, output_path: str):
        self.output_path = output_path
