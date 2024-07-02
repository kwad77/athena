# athena/services/document_service.py

import os
import shutil
from PyPDF2 import PdfReader
from docx import Document

class DocumentService:
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.documents_folder = os.path.join(self.working_directory, "documents")
        os.makedirs(self.documents_folder, exist_ok=True)

    def process_document(self, file_path):
        try:
            # Copy the file to the documents folder
            new_file_path = os.path.join(self.documents_folder, os.path.basename(file_path))
            shutil.copy2(file_path, new_file_path)

            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.pdf':
                return self.process_pdf(new_file_path)
            elif file_extension == '.docx':
                return self.process_docx(new_file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")

    def process_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

    def process_docx(self, file_path):
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def set_working_directory(self, new_directory):
        self.working_directory = new_directory
        self.documents_folder = os.path.join(self.working_directory, "documents")
        os.makedirs(self.documents_folder, exist_ok=True)