from core.jd_analyzer.jd_processor import JDProcessor

from core.resume_analyzer.pdf_parser import PDFParser

from docx import Document


class JDService:

    def __init__(
            self
    ):
        self.processor = JDProcessor()

        self.pdf_parser = PDFParser()

    async def process_jd_from_text(
            self,
            jd_text
    ):

        cleaned_text = self.processor.clean_jd_text(jd_text)

        return cleaned_text

    async def process_jd_from_file(
            self,
            file_path
    ):

        if file_path.endswith(".pdf"):

            raw_text = self.pdf_parser.extract_text(file_path)

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            raw_text = "\n".join(
                para.text for para in doc.paragraphs
            )

        elif file_path.endswith(".txt"):

            with open(file_path, "r", encoding="utf-8") as f:

                raw_text = f.read()

        cleaned_text = self.processor.clean_jd_text(raw_text)

        return cleaned_text