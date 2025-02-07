from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class SectionData:  # this class will be having the data section wise it has section number in numeric form
    section_number: int
    chapter_name: str  # section name
    full_text: str  # complete text in that doc
    tables: List[Dict] = field(default_factory=list)  # tables in this section
    key_findings: str = ""  # this will be an AI generated summary for the section
    pages: str = ""  # good info to have


@dataclass
class CompanyData:
    company_name: str  # company name as the file is for the company, and it's better to just have
    # written just once (will save space too)
    sections: List[SectionData] = field(default_factory=list)  #section data


@dataclass
class DocumentData:  #this data class is for the document processor
    full_text: str
    file_path: str
