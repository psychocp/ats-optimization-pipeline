from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text from an uploaded PDF file stream cleanly.
    This reads the binary data straight from memory without saving 
    the file to your hard drive, making it fast and efficient.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = ""
        
        # Loop through every single page of the PDF and grab the text
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
        # Strip out any empty leading/trailing whitespace
        return extracted_text.strip()
        
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {str(e)}")