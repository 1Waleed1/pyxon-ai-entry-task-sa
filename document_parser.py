import fitz
from docx import document
import os

class DocumentParser:

    def __init__(self):
        pass
    
    def read_file(self,file_path):
        """
        Main entry point for reading files. It checks the extension 
        and routes the file to the appropriate helper method.
        """

        _, file_extension = os.path.splitext(file_path)
        
        file_extension=file_extension.lower()
        
        if file_extension ==".pdf":
            return self._read_pdf(file_path)
        
        elif file_extension in [".doxc",".doc"]: # Supporting both older .doc and modern .docx formats
            return self._read_document(file_path)
        
        else:
            return "Error unsupported formats " # Simple error handling for unsupported formats
    
    def _read_pdf(self,file_path):
        """
        Helper method that iterates through PDF pages and 
        consolidates all text into a single string.
        """

        text=""
        
        pdf_document=fitz.open(file_path)
        
        for page_num in range(len(pdf_document)): # Loop through each page to ensure no content is missed
            page=pdf_document[page_num]
            text+=page.get_text()
        return text
    
    def _read_document(self,file_path):

        """
        Helper method for Word files. It extracts text paragraph 
        by paragraph to maintain the document's natural flow.
        """

        text=""

        doc=document(file_path)
        
        for paragraph in doc.paragraphs:
            text+=paragraph.text + "\n"
        
        return text
    
    def create_chunks(self,text,chunk_size=500,overlap=100):

        """
        Sliding window implementation for text chunking. 
        Crucial for keeping context alive across chunks in RAG systems.
        """
        
        chunks = []
        
        step = chunk_size-overlap # Calculating step size to account for the overlapping text

        for i in range(0 , len(text) , step):
            chunk= text[i : i + chunk_size]
            chunks.append(chunk)
        
        return chunks










