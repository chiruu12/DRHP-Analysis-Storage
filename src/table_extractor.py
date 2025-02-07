import tabula


class TableExtractor:
    # I could have used ocr based table extractor but it wasn't mentioned if we can use it or not so
    # made a simple table extractor using tabula
    @staticmethod
    def extract_tables(pdf_path: str, pages: str = 'all') -> list:
        try:
            dfs = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)
        except Exception as e:
            print("Error reading tables with Tabula:", e)
            return []
        tables = []
        for df in dfs:
            tables.append(df.to_dict(orient='records'))
        return tables
