from PyPDF2 import PdfReader

class FileParser:
    """
    Extracts text from uploaded files (PDF or TXT).
    """

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """
        Read a PDF file and extract all text.
        """
        reader = PdfReader(file_path)
        text = []
        for page in reader.pages:
            if page.extract_text():
                text.append(page.extract_text())
        return "\n".join(text)

    @staticmethod
    def parse_txt(file_path: str) -> str:
        """
        Read a plain text file.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
