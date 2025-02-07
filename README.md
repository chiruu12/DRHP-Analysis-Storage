# DRHP Analysis & Storage

## Overview

This project analyzes Draft Red Herring Prospectus (DRHP) documents—regulatory filings by companies planning to go public—to extract key insights such as financials, risk factors, business strategies, and operational details. The structured data is then enriched with AI-generated summaries and vector embeddings for efficient retrieval and analysis.
this project can be made better with resources currently it is made for free.

## Objectives

- **Extract** key details from DRHP documents, including:
  - Section Number
  - Chapter Name
  - Company Name
  - Full Text
  - Tables (structured tabular data) (used tabula for that)
  - Key Findings (AI-generated summaries)
- **Generate vector embeddings** for the key findings using an embedding model.
- **Store the processed data** in a vector database for efficient similarity search and retrieval.

## Assignment Tasks

1. **Download DRHP Documents:**  
   Download 5 DRHP documents from the SEBI website.

2. **Parse and Structure Data:**  
   Use Python scripts to extract the full text from the PDFs and structure the data into JSON/CSV. The structured data includes details such as company name, section number, chapter name, full text, and any tabular data.

3. **AI Summarization:**  
   Generate comprehensive AI-based summaries for each section using the Gemini API (Google Generative AI).

4. **Vector Embedding:**  
   Generate vector embeddings for each section’s key findings using a SentenceTransformer model.

5. **Store in a Vector Database:**  
   Store the embeddings in a vector database (using FAISS) to support efficient similarity search and retrieval.

## Deliverables

- **Python Scripts:**
  - **doc_processor.py:** Downloads and extracts text from DRHP PDFs.
  - **company_data_class:** it hold the data structures made for this project
  - **data_extractor.py:** Parses and structures the extracted data.
  - **data_extractor.py:** Parses and structures the extracted Table. will be making a better and more proficient one using ocr.
  - **section_summarizer.py:** Generates AI-based summaries for each section using together. 
  - **vector_embedder.py:** Generates vector embeddings and stores them in a FAISS index.
  - **Pipeline.py:** Orchestrates the entire pipeline.
- **Output Files:**
  - JSON/CSV output containing the structured DRHP data.
  - A vector database (FAISS index) populated with embedded key findings.

## Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root and add your Gemini API key:

```
TOGETHER_API_KEY = your_api_key_here
```

## Usage

1. **Download the DRHP PDFs:**  
   Place the downloaded DRHP documents in the `docs/` folder.

2. **Set output and input path**
    Set the input and output path in the main.py file
3. **Run the Pipeline:**  
   Execute the pipeline script to process PDFs, extract structured data, generate summaries, and store vector embeddings:
   ```bash
   python main.py
   ```
   
4. **Query the Vector Database:**  
   Use the provided vector embedder scripts to perform similarity searches on the stored embeddings.
