import os
import time
from dotenv import load_dotenv
from together import Together
from company_data_class import CompanyData


class SectionSummarizer:
    def __init__(self, model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
        load_dotenv()  # Loads environment variables from .env or Colab Secrets
        self.client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
        self.model = model

    def _chunk_text(self, text: str, max_chars: int = 24000, overlap: int = 400) -> list:
        total_length = len(text)
        step = max_chars - overlap
        chunks = []
        for i in range(0, total_length, step):
            chunk = text[i:i+max_chars]
            chunks.append(chunk)
        return chunks

    def _final_summarize(self, text: str, company_name: str, max_chars: int = 24000, overlap: int = 400, max_tokens: int=500) -> str:
        if len(text) <= max_chars:
            prompt = (
                f"As a highly experienced financial analyst at {company_name}, please provide a concise "
                "and comprehensive final summary of the following text:\n\n" + text
            )
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        else:
            # Determine number of chunks needed (at least 2)
            num_chunks = (len(text) // max_chars) + 1
            chunks = self._chunk_text(text, max_chars=max_chars, overlap=overlap)
            chunk_summaries = []
            for i, chunk in enumerate(chunks):
                prompt = (
                    f"As a highly experienced financial analyst at {company_name}, please provide a concise summary of the following text:\n\n" + chunk
                )
                messages = [{"role": "user", "content": prompt}]
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens
                )
                summary = response.choices[0].message.content.strip()
                chunk_summaries.append(summary)
                print(f"Final summarization chunk {i+1}/{len(chunks)} completed.")
                time.sleep(2)
            combined = " ".join(chunk_summaries)
            print("summarizing the combined final summaries...")
            return self._final_summarize(combined, company_name, max_chars, overlap, max_tokens)

    def summarize_text(self, text: str, company_name: str) -> str:
        print(f"Getting summary for company {company_name}: {text[:20]}...")
        # Split the text into 8 chunks with overlap
        chunks = self._chunk_text(text, max_chars=20000, overlap=400)
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            prompt = (
                f"As a highly experienced financial analyst at {company_name}, you are tasked with reviewing "
                "the following text and crafting a comprehensive summary. Ensure that you capture every important "
                "detail, including key financial insights, risk factors, business strategies, and operational "
                "nuances. Do not omit any critical information, and provide a clear, detailed overview that "
                "would enable investors and analysts to make well-informed decisions.\n\n" + chunk
            )
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=400
            )
            summary = response.choices[0].message.content.strip()
            chunk_summaries.append(summary)
            print(f"Chunk {i+1}/{len(chunks)} summarized.")
            time.sleep(0.5)
        combined_summary = " ".join(chunk_summaries)
        print("Combining chunk summaries and generating final summary...")
        final_summary = self._final_summarize(combined_summary, company_name, max_chars=20000, overlap=400,
                                              max_tokens=400)
        return final_summary

    def summarize_sections(self, company_data: CompanyData) -> CompanyData:
        for section in company_data.sections:
            if section.full_text and section.full_text.strip():
                section.key_findings = self.summarize_text(section.full_text, company_data.company_name)
        return company_data
