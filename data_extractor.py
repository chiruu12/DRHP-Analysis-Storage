import re
from company_data_class import CompanyData, SectionData, DocumentData
from table_extractor import TableExtractor
import fitz


class DataExtractor:
    @staticmethod
    def roman_to_int(roman) -> int:
        roman = roman.upper()
        roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_numerals.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        return result

    @staticmethod
    def preprocess_text(text: str) -> str:
        """some docs might have Sections written as SECTION I: we are removing the : form the doc for such cases
        """
        processed_text = re.sub(r'(SECTION\s+[IVXLCDM]+)\s*:', r'\1', text, flags=re.IGNORECASE)
        return processed_text

    @staticmethod
    def extract_company_name(text: str) -> str:
        pattern = r'^([A-Z0-9\s,&\.\-]+)\s*\n\s*Corporate Identity Number:?'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else "Unknown Company"

    @staticmethod
    def extract_toc_entries(text: str) -> list:
        toc_start = text.find("TABLE OF CONTENTS")
        if toc_start == -1:
            return []
        toc_block = text[toc_start:toc_start + 6500]
        lines = toc_block.splitlines()
        entries = []
        pattern = re.compile(
            r'^(SECTION\s+([IVXLCDM]+)):?\s*[-–]\s*([A-Z\s,&\-]+?)\s+\.{3,}\s+(\d+)\s*$',
            re.MULTILINE
        )
        for line in lines:
            line = line.strip()
            m = pattern.match(line)
            if m:
                entries.append(
                    {"roman": m.group(2).strip(), "chapter_name": m.group(3).strip(), "page": m.group(4).strip()})
        return entries

    @staticmethod
    def extract_section_full_text(text: str, current_label: str, next_label: str = None) -> str:
        first_occurrence = text.find(current_label)
        if first_occurrence == -1:
            return ""
        second_occurrence = text.find(current_label, first_occurrence + len(current_label))
        if second_occurrence == -1:
            second_occurrence = first_occurrence
        start_index = second_occurrence

        if next_label:
            next_first = text.find(next_label, start_index)
            if next_first == -1:
                end_index = len(text)
            else:
                next_second = text.find(next_label, next_first + len(next_label))
                end_index = next_second if next_second != -1 else len(text)
        else:
            end_index = len(text)
        return text[start_index:end_index].strip()

    @classmethod
    def get_company_data(cls, doc_data: DocumentData) -> CompanyData:
        if not isinstance(doc_data, DocumentData):
            raise TypeError(f"Expected DocumentData object but got {type(doc_data)}")

        text = cls.preprocess_text(doc_data.full_text)
        company_name = cls.extract_company_name(text)
        toc_entries = cls.extract_toc_entries(text)
        sections_data = []
        pages_list = [int(entry["page"]) for entry in toc_entries]

        for i, entry in enumerate(toc_entries):
            current_label = f"SECTION {entry['roman']} "
            next_label = None
            if i + 1 < len(toc_entries):
                next_entry = toc_entries[i + 1]
                next_label = f"SECTION {next_entry['roman']} "

            section_text = cls.extract_section_full_text(text, current_label, next_label)
            start_page = pages_list[i]

            if i + 1 < len(pages_list):
                end_page = pages_list[i + 1] - 1
                pages_str = f"{start_page}-{end_page}"
            else:
                doc = fitz.open(doc_data.file_path)
                num_pages = doc.page_count
                doc.close()
                pages_str = f"{start_page}-{num_pages}"

            sections_data.append(
                SectionData(
                    section_number=cls.roman_to_int(entry["roman"]),
                    chapter_name=entry["chapter_name"],
                    full_text=section_text,
                    tables=TableExtractor.extract_tables(pdf_path=doc_data.file_path, pages=pages_str),
                    key_findings="",
                    pages=pages_str
                )
            )
        return CompanyData(company_name=company_name, sections=sections_data)